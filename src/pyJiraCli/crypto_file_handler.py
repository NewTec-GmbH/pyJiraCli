"""crpyto module for information file handling.
   provides function to encrypt and decrypt user or server information
   to and from files"""
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
from enum import IntEnum

from cryptography.fernet import Fernet

from pyJiraCli.retval import Ret
################################################################################
# Variables
################################################################################
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

class DataType (IntEnum):
    """"data_type to concern between which data information will be encrypted
        or decrypted with the encrypt_information() and 
        decrypt_information() function"""
    DATATYPE_USER_INFO       = 0
    DATATYPE_TOKEN_INFO      = 1
    DATATYPE_SERVER          = 2
    DATATYPE_SERVER_DEFAULT  = 3

data_keys = {
    DataType.DATATYPE_USER_INFO      : ("user", "pw"),
    DataType.DATATYPE_TOKEN_INFO     : ("user", "token"),
    DataType.DATATYPE_SERVER         : ("url", None),
    DataType.DATATYPE_SERVER_DEFAULT : ("url", None)
}
################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################
def _get_path_to_login_folder():

    user_info_path = os.path.expanduser("~") + PATH_TO_FOLDER
    if not os.path.exists(user_info_path):
        os.makedirs(user_info_path)
    return user_info_path

def _get_device_root_key():
    # check which os is being used
    if "nt" in os.name:
        _uuid = sub.check_output(UUID_CMD_WIN).split()[-1]
    else:
        _uuid = sub.check_output(UUID_CMD_UNIX).replace('"', '\n').split()[-1]

    hasher = hashlib.sha3_512(_uuid)
    hex_string = hasher.hexdigest().encode()

    byte_data = bytes.fromhex(hex_string.decode())  # Decode hexadecimal string to bytes
    return base64.urlsafe_b64encode(byte_data)[-45:-1]

def _get_user_data_str(user, pw, expires):
    data = f'{"{"}\n' + \
           f'   "user": "{user}",\n' + \
           f'   "pw": "{pw}"\n' + \
           f'   "expires": "{expires}"\n' + \
           f'{"}"}'    
    return data

def _get_token_data_str(user, token, expires):
    data = f'{"{"}\n' + \
           f'   "user": "{user}",\n' + \
           f'   "token": "{token}",\n' + \
           f'   "expires": "{expires}"\n' + \
           f'{"}"}'    
    return data

def _get_server_data_str(url, data, expires):
    data = f'{"{"}\n' + \
           f'   "url": "{url}",\n' + \
           f'   "expires": "{expires}"\n' + \
           f'{"}"}'    
    return data

data_str_funcs = { \
    DataType.DATATYPE_USER_INFO      : _get_user_data_str,
    DataType.DATATYPE_TOKEN_INFO     : _get_token_data_str,
    DataType.DATATYPE_SERVER         : _get_server_data_str,
    DataType.DATATYPE_SERVER_DEFAULT : _get_server_data_str,
}

def _get_file_paths(data_type):
    if data_type is DataType.DATATYPE_USER_INFO:
        file_path_data = USER_INFO_FILE
        file_path_key = USER_KEY_FILE

    elif data_type is DataType.DATATYPE_TOKEN_INFO:
        file_path_data = TOKEN_INFO_FILE
        file_path_key = TOKEN_KEY_FILE

    elif data_type is DataType.DATATYPE_SERVER:
        file_path_data = SERVER_INFO_FILE
        file_path_key = SERVER_KEY_FILE

    elif data_type is DataType.DATATYPE_SERVER_DEFAULT:
        file_path_data = SERVER_DEFAULT_INFO_FILE
        file_path_key = SERVER_DEFAULT_KEY_FILE

    return file_path_data, file_path_key

def _get_data_str(data1, data2, expires, data_type):
    return data_str_funcs[data_type](data1, data2, expires)

def _read_encrypted_data(path_data, path_key, data_type):

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
        ret_status = Ret.RET_ERROR_INFO_FILE_EXPIRED

    return data1, data2, ret_status

def encrypt_information(data1, data2, expires, data_type):
    """ encrypt userinformation to file
        
    param:
    data1: data field for encryption
    data2: optional data field for encryption
    expires: expiration date of the data
    data_type: which data_type is to be written (user, token, server)

    returns:
    the exit status of the module
    """

    # get data structure for user data unencrypted
    folderpath = _get_path_to_login_folder()
    file_path_data, file_path_key =_get_file_paths(data_type)
    data_str = _get_data_str(data1, data2, expires, data_type)

    # generate new key for user data
    file_key = Fernet.generate_key()

    f_writer_key = Fernet(_get_device_root_key())
    f_writer_data = Fernet(file_key)

    encrypted_key_info = f_writer_key.encrypt(file_key)
    encrypted_data_info = f_writer_data.encrypt(data_str.encode(encoding='utf-8'))

    try:
        with open(folderpath + file_path_key, "w", encoding='utf-8') as outfile:
            outfile.write(f'{encrypted_key_info}'[2:-1])
        outfile.close()

        with open(folderpath + file_path_data, "w", encoding='utf-8') as outfile:
            outfile.write(f'{encrypted_data_info}'[2:-1])
        outfile.close()

    except (OSError, IOError) as e:
        # print exception
        print(e)
        return Ret.RET_ERROR_FILE_OPEN_FAILED

    return Ret.RET_OK

def decrypt_information(data_type):
    """ decrypt and return data from file
        
        param: 
        data_type: the data_type that shall be decrypted(user, token, server)
        
        return:
        the requested data or None
        exit status of the module"""

    ret_status = Ret.RET_OK

    data1 = None
    data2 = None

    file_name_data, file_name_key = _get_file_paths(data_type)

    filepath_data =  _get_path_to_login_folder() + file_name_data
    filepath_key =  _get_path_to_login_folder() + file_name_key

    data1, data2, ret_status = _read_encrypted_data(filepath_data, filepath_key, data_type)

    return data1, data2, ret_status

def delete(data_type):
    """ delete login info
        
        param:
        data_type: which data shall be removed
    """

    folderpath = _get_path_to_login_folder()
    file_path_data, file_path_key = _get_file_paths(data_type)

    if os.path.exists(folderpath + file_path_data):
        os.remove(folderpath + file_path_data)

    if os.path.exists(folderpath + file_path_key):
        os.remove(folderpath + file_path_key)

def delete_all():
    """"delete all info files and folder"""

    delete(DataType.DATATYPE_USER_INFO)
    delete(DataType.DATATYPE_TOKEN_INFO)
    delete(DataType.DATATYPE_SERVER)
    delete(DataType.DATATYPE_SERVER_DEFAULT)
    os.removedirs(PATH_TO_FOLDER)
