""" Crpyto module for information file handling.
    Provides function to encrypt and decrypt user or server information
    to and from files.
"""
# BSD 3-Clause License
#
# Copyright (c) 2024, NewTec GmbH
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

################################################################################
# Imports
################################################################################
import os
import json
import subprocess as sub
import hashlib
import time
import base64
import ctypes

from cryptography.fernet import Fernet

from pyJiraCli.ret import Ret
from pyJiraCli.data_type import DataType
################################################################################
# Variables
################################################################################
FILE_ATTRIBUTE_HIDDEN = 0x02

PATH_TO_FOLDER   = "\\.pyJiraCli\\.logindata"

USER_INFO_FILE   = "\\.user.data"
USER_KEY_FILE    = "\\.user_key.data"

TOKEN_INFO_FILE  = "\\.token.data"
TOKEN_KEY_FILE  = "\\.token_key.data"

SERVER_INFO_FILE = "\\.server.data"
SERVER_KEY_FILE  = "\\.server_key.data"

SERVER_DEFAULT_INFO_FILE = "\\.server_default.data"
SERVER_DEFAULT_KEY_FILE  = "\\.server_default_key.data"

TMP_FILE         = "\\.tmp.json"

UUID_CMD_WIN  = "wmic csproduct get uuid"
UUID_CMD_UNIX = "blkid"

data_keys = {
    DataType.DATATYPE_USER_INFO      : ("user", "pw"),
    DataType.DATATYPE_TOKEN_INFO     : ("user", "token"),
    DataType.DATATYPE_SERVER         : ("url", None),
    DataType.DATATYPE_SERVER_DEFAULT : ("url", None)
}

file_paths = {
    DataType.DATATYPE_USER_INFO      : (USER_INFO_FILE, USER_KEY_FILE),
    DataType.DATATYPE_TOKEN_INFO     : (TOKEN_INFO_FILE, TOKEN_KEY_FILE),
    DataType.DATATYPE_SERVER         : (SERVER_INFO_FILE, SERVER_KEY_FILE),
    DataType.DATATYPE_SERVER_DEFAULT : (SERVER_DEFAULT_INFO_FILE, SERVER_DEFAULT_KEY_FILE)
}

data_str_funcs = {
    DataType.DATATYPE_USER_INFO      : None,
    DataType.DATATYPE_TOKEN_INFO     : None,
    DataType.DATATYPE_SERVER         : None,
    DataType.DATATYPE_SERVER_DEFAULT : None,
}

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################
def encrypt_information(data1, data2, expires, data_type):
    """ Save information in a dictionary with max 2 key-value pairs.
        The expiration date will be added in the dictionary too, when decrypting
        information, the module will check if the data is expired. 
        Encrypted information is saved to a .data file.
        
    Args:
        data1 (str):            data field for encryption
        data2 (str):            optional data field for encryption
        expires (float):        expiration date of the data
        data_type (DataType):   which data_type is to be written (user, token, server)

    Returns:
        Ret:   Ret.RET_OK if succesfull, corresponding error code if not
    """

    # get file paths
    file_path_data, file_path_key = file_paths[data_type]

    file_path_data = _get_path_to_login_folder() + file_path_data
    file_path_key  = _get_path_to_login_folder() + file_path_key

    # get data structure for user data unencrypted
    data_str = _get_data_str(data_type, data1, data2, expires)

    # generate new key for user data
    file_key = Fernet.generate_key()

    f_writer_key = Fernet(_get_device_root_key())
    f_writer_data = Fernet(file_key)

    encrypted_key_info = f_writer_key.encrypt(file_key)
    encrypted_data_info = f_writer_data.encrypt(data_str.encode(encoding='utf-8'))

    if os.path.exists(file_path_data):
        os.remove(file_path_data)

    if os.path.exists(file_path_key):
        os.remove(file_path_key)

    try:
        with open(file_path_key, "w", encoding='utf-8') as outfile:
            outfile.write(f'{encrypted_key_info}'[2:-1])
        outfile.close()

        ctypes.windll.kernel32.SetFileAttributesW(file_path_key,
                                                  FILE_ATTRIBUTE_HIDDEN)

        with open(file_path_data, "w", encoding='utf-8') as outfile:
            outfile.write(f'{encrypted_data_info}'[2:-1])
        outfile.close()

        ctypes.windll.kernel32.SetFileAttributesW(file_path_data,
                                                  FILE_ATTRIBUTE_HIDDEN)

    except (OSError, IOError) as e:
        # print exception
        print(e)
        return Ret.RET_ERROR_FILE_OPEN_FAILED

    return Ret.RET_OK

def decrypt_information(data_type):
    """ Decrypt and return the data pair of a login file.
        The information which will be decrypted depends on the data_type
        with which the function is called.
        
    Args: 
        data_type (DataType):   the data_type that shall be decrypted
                                (user, token, server, default servers)
        
    Returns:
        str:   the decrypted first data value or None
        str:   the decrypted second data value or None
        Ret:   Ret.RET_OK if succesfull, corresponding error code if not
    """

    ret_status = Ret.RET_OK

    data1 = None
    data2 = None

    if data_type in file_paths:
        file_name_data, file_name_key = file_paths[data_type]

        filepath_data =  _get_path_to_login_folder() + file_name_data
        filepath_key =  _get_path_to_login_folder() + file_name_key

        data1, data2, ret_status = _read_encrypted_data(filepath_data, filepath_key, data_type)

    else:
        ret_status = Ret.RET_ERROR

    return data1, data2, ret_status

def delete(data_type):
    """ Delete the stored login files of a DataType.
        
    Args:
        data_type (Datatype):   which data shall be removed
    """

    folderpath = _get_path_to_login_folder()
    file_path_data, file_path_key = file_paths[data_type]

    if os.path.exists(folderpath + file_path_data):
        os.remove(folderpath + file_path_data)

    if os.path.exists(folderpath + file_path_key):
        os.remove(folderpath + file_path_key)

def delete_all():
    """ Delete all info files and folder
        of the login files
    """

    delete(DataType.DATATYPE_USER_INFO)
    delete(DataType.DATATYPE_TOKEN_INFO)
    delete(DataType.DATATYPE_SERVER)
    delete(DataType.DATATYPE_SERVER_DEFAULT)
    os.removedirs(_get_path_to_login_folder())


def _get_path_to_login_folder():
    """ Returns the path to the pyJiraCli tool data.
        All tool data (logindata/configs) is stored in the users
        home directory.

    Returns:
        user_info_path (str): the path to the data folder
    """
    user_info_path = os.path.expanduser("~") + PATH_TO_FOLDER

    if not os.path.exists(user_info_path):
        os.makedirs(user_info_path)
        ctypes.windll.kernel32.SetFileAttributesW(user_info_path,
                                                  FILE_ATTRIBUTE_HIDDEN)
    return user_info_path

def _get_device_root_key():
    """ Return the device root key, 
        to provided a safe root key this module uses the user/device unique uuid of the system
        the uuid is first hashed and then stripped to 32 bytes

    Returns:
        bytes: the last 32 bytes of the uuid of the system hashed and encoded
    """
    # check which os is being used
    if "nt" in os.name:
        _uuid = sub.check_output(UUID_CMD_WIN).split()[-1]
    else:
        _uuid = sub.check_output(UUID_CMD_UNIX).replace('"', '\n').split()[-1]

    hasher = hashlib.sha3_512(_uuid)
    hex_string = hasher.hexdigest().encode()

    byte_data = bytes.fromhex(hex_string.decode())  # Decode hexadecimal string to bytes
    root_key = base64.urlsafe_b64encode(byte_data)[-45:-1]

    return root_key

def _read_encrypted_data(path_data, path_key, data_type):
    """ Read the encrypted data of one of the login files.
        If the information is expired, the files will be deleted after the
        data was retrieved.

    Args:
        path_data (str):        path to the encrypted data file
        path_key (str):         path to the encrypted key file
        data_type (DataType):   the dataType that shall be decrypted   

    Returns:
        str:   the first data-value which was stored in the encrypted file
        str:   the second data-value which was stored in the encrypted file
        Ret:   Ret.RET_OK if succesfull, corresponding error code if not
    """
    ret_status = Ret.RET_OK

    data1 = None
    data2 = None
    expires = None
    f_reader_key = Fernet(_get_device_root_key())

    if os.path.exists(path_data):
        try:
            with open(path_key, "r", encoding='utf-8') as file:
                key_data = f_reader_key.decrypt(file.readline())
            file.close()

            f_reader_data = Fernet(key_data)

            with open(path_data, 'r', encoding='utf-8') as file:
                decrypted_data = f_reader_data.decrypt(bytes(file.readline(), encoding='utf-8'))
            file.close()

            tmp_file = _get_path_to_login_folder() + TMP_FILE

            with open(tmp_file, 'w', encoding='utf-8') as file:
                file.write(str(decrypted_data.decode('utf-8')))
            file.close()

            with open(tmp_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            file.close()

            os.remove(tmp_file)

            # read data
            data1 = data[data_keys[data_type][0]]
            if data_keys[data_type][1] is not None:
                data2 = data[data_keys[data_type][1]]
            expires = float(data["expires"])

        except (OSError, IOError) as e:

            # always remove the tmp file
            if os.path.exists(tmp_file):
                os.remove(tmp_file)

            # print exception
            print(e)
            ret_status = Ret.RET_ERROR_FILE_OPEN_FAILED
    else:
        ret_status = Ret.RET_ERROR_NO_USERINFORMATION

    if expires is not None and \
       expires < time.time():
        delete(data_type)
        print(data_type, ": the stored information has expired and was deleted")

        ret_status = Ret.RET_ERROR_INFO_FILE_EXPIRED

    return data1, data2, ret_status

def _get_data_str(data_type, data1, data2, expires):
    """ Prepare token data for encryption.
    
    Args:
        data1 (str):         user or url, depending on datatype
        data2 (str):         pw, token or none, depending on datatype
        expires (float):     expiration date of the data
    
    Returns:
        str:    formated json string with key-value pairs of the data
    """
    if data_type not in (DataType.DATATYPE_SERVER, DataType.DATATYPE_SERVER_DEFAULT):
        data = f'{"{"}\n' + \
               f'   {data_keys[data_type][0]}: "{data1}",\n' + \
               f'   {data_keys[data_type][1]}: "{data2}",\n' + \
               f'   "expires": "{expires}"\n' + \
               f'{"}"}'    
    else:
        data = f'{"{"}\n' + \
               f'   {data_keys[data_type][0]}: "{data1}",\n' + \
               f'   "expires": "{expires}"\n' + \
               f'{"}"}'
    return data
