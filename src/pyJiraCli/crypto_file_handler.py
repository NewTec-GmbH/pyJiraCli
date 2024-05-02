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
from pyJiraCli.file_handler import FileHandler as File
from pyJiraCli.data_type import DataType, DataMembers
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
    DataType.DATATYPE_TOKEN_INFO     : ("token", None),
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
class Crypto:
    """ This class handles all encryption and decryption operations
    """
    def __init__(self):
        self._data1 = None
        self._data2 = None
        self._expired:bool = False

        self._file_data = File()
        self._file_key = File()
        self._root_key = _get_device_root_key()
        self._homepath = _get_path_to_login_folder()

    def set_data(self, data1:str, data2:str = None) -> None:
        """ Set the data which shall be encrypted.

        Args:
            data1 (str): First data of the pair.
            data2 (str): Second data of pair (default is None for server or token data). 
        """
        self._data1 = data1
        self._data2 = data2

    def get_data(self, data_mem:DataMembers = DataMembers.DATA_MEM_1) -> str:
        """ Return the data after decryption.

        Args:
            data_nr (DataMembers): Decides if data1 or data2 is returned. 

        Returns:
           str: The stored data in class member data1 or data2.
        """
        if data_mem is DataMembers.DATA_MEM_2:
            ret_data = self._data2
        else:
            ret_data = self._data1

        return ret_data

    def check_if_expired(self) -> bool:
        """ Check if the decrypted data is expired 
            or not. 

        Returns:
            bool: Return True if data is expired or False otherwise or when no data was decrypted.
        """
        return self._expired

    def encrypt_information(self, expires:float, data_type:DataType) -> Ret:
        """ Save information in a dictionary with max 2 key-value pairs.
            The expiration date will be added in the dictionary too, when decrypting
            information, the module will check if the data is expired. 
            Encrypted information is saved to a .data file.

        Args:
            expires (float):        Expiration date of the data in epoch seconds.
            data_type (DataType):   Which data_type is to be written (userinfo, token, server).

        Returns:
        Ret:   Returns Ret.RET_OK if succesfull or the corresponding error code if not.
        """
        # get file paths
        file_path_data, file_path_key = file_paths[data_type]

        ret_status = self._file_data.set_filepath(self._homepath + file_path_data)
        ret_status = self._file_key.set_filepath(self._homepath + file_path_key)

        if ret_status == Ret.RET_OK:
            # get data structure for user data unencrypted
            data_str = _get_data_str(self._data1, self._data2, expires, data_type)

            # generate new key for user data
            data_key = Fernet.generate_key()

            f_writer_key = Fernet(self._root_key)
            f_writer_data = Fernet(data_key)

            try:
                encrypted_key_info = f_writer_key.encrypt(data_key)
                encrypted_data_info = f_writer_data.encrypt(data_str.encode(encoding='utf-8'))

                ret_status = self._file_key.write_file(encrypted_key_info \
                                                       .decode(encoding='utf-8'))
                ret_status = self._file_data.write_file(encrypted_data_info \
                                                        .decode(encoding='utf-8'))

            except Exception as e: # pylint: disable=broad-except
                print(e)
                ret_status = Ret.RET_ERROR

            if ret_status != Ret.RET_OK:
                self._file_key.delete_file()
                self._file_data.delete_file()

            self._file_data.hide_file()
            self._file_key.hide_file()

            self._file_key.close_file()
            self._file_data.close_file()

        return ret_status

    def decrypt_information(self, data_type:DataType) -> Ret:
        """ Decrypt and return the data pair of a login file.
            The information which will be decrypted depends on the data_type
            with which the function is called.

        Args: 
            data_type (DataType):   TRhe data_type that shall be decrypted
                                    (user, token, server, default servers).

        Returns:
        Ret:   Returns Ret.RET_OK if succesfull or the corresponding error code if not.
        """

        ret_status = Ret.RET_OK

        if data_type in file_paths:
            file_name_data, file_name_key = file_paths[data_type]

            filepath_data = self._homepath + file_name_data
            filepath_key  = self._homepath + file_name_key

            ret_status = self._read_encrypted_data(filepath_data,
                                                   filepath_key,
                                                   data_type)

        else:
            ret_status = Ret.RET_ERROR

        return ret_status

    def delete(self, data_type) -> None:
        """ Delete the stored login files of a DataType.

        Args:
            data_type (Datatype):   Which data shall be removed.
        """

        folderpath = _get_path_to_login_folder()
        file_path_data, file_path_key = file_paths[data_type]

        if os.path.exists(folderpath + file_path_data):
            os.remove(folderpath + file_path_data)

        if os.path.exists(folderpath + file_path_key):
            os.remove(folderpath + file_path_key)

    def delete_all(self) -> None:
        """ Delete all info files and folder
            of the login files
        """

        self.delete(DataType.DATATYPE_USER_INFO)
        self.delete(DataType.DATATYPE_TOKEN_INFO)
        self.delete(DataType.DATATYPE_SERVER)
        self.delete(DataType.DATATYPE_SERVER_DEFAULT)
        os.removedirs(_get_path_to_login_folder())

    def _read_encrypted_data(self, path_data:str, path_key:str, data_type:DataType) -> Ret:
        """ Read the encrypted data of one of the login files.
            If the information is expired, the files will be deleted after the
            data was retrieved.

        Args:
            path_data (str):        Path to the encrypted data file.
            path_key (str):         Path to the encrypted key file.
            data_type (DataType):   The dataType that shall be decrypted.   

        Returns:
        Ret:   Returns Ret.RET_OK if succesfull or the corresponding error code if not.
        """
        ret_status = Ret.RET_OK
        expires = None
        tmp_file = File()

        ret_status = self._file_data.set_filepath(path_data)
        ret_status = self._file_key.set_filepath(path_key)
        ret_status = tmp_file.set_filepath(self._homepath + TMP_FILE)

        if ret_status == Ret.RET_OK:
            ret_status = self._file_key.read_file()
            ret_status = self._file_data.read_file()

        if ret_status == Ret.RET_OK:
            f_reader = Fernet(self._root_key)

            try:

                key_data = f_reader.decrypt(self._file_key.get_file_content() \
                                            .encode(encoding='utf-8'))

                f_reader = Fernet(key_data)
                data = f_reader.decrypt(self._file_data.get_file_content().encode(encoding='utf-8'))

                tmp_file = File()
                tmp_file.set_filepath(self._homepath + TMP_FILE)

                ret_status = tmp_file.write_file(data.decode(encoding='utf-8'))
                tmp_file.close_file()

            except Exception as e: # pylint: disable=broad-except
                print(e)
                ret_status = Ret.RET_ERROR

        if ret_status == Ret.RET_OK:
            ret_status = tmp_file.open_file(file_mode='r')

        if ret_status == Ret.RET_OK:
            data = json.load(tmp_file.get_file())

            # read data
            self._data1 = data[data_keys[data_type][0]]

            if data_keys[data_type][1] is not None:
                self._data2 = data[data_keys[data_type][1]]

            if "expires" in data:
                expires = float(data["expires"])

        else:
            ret_status = Ret.RET_ERROR_NO_USERINFORMATION

        if expires is not None and \
           expires < time.time():
            self._expired = True

        self._file_key.close_file()
        self._file_data.close_file()
        tmp_file.close_file()
        tmp_file.delete_file()

        return ret_status

################################################################################
# Functions
################################################################################
def _get_device_root_key() -> bytes:
    """ Return the device root key, 
        to provided a safe root key this module uses the user/device unique uuid of the system
        the uuid is first hashed and then stripped to 32 bytes
    
    Returns:
        bytes: The last 32 bytes of the uuid of the system hashed and encoded.
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

def _get_path_to_login_folder() -> str:
    """ Returns the path to the pyJiraCli tool data.
        All tool data (logindata/configs) is stored in the users
        home directory.
    
    Returns:
        str: The path to the login data folder.
    """

    user_info_path = os.path.expanduser("~") + PATH_TO_FOLDER

    if not os.path.exists(user_info_path):
        os.makedirs(user_info_path)
        ctypes.windll.kernel32.SetFileAttributesW(user_info_path,
                                                  FILE_ATTRIBUTE_HIDDEN)
    return user_info_path

def _get_data_str(data1:str, data2:str, expires:float, data_type:DataType) -> str:
    """ Prepare token data for encryption.

    Args:
        data1 (str):         User, token or url, depending on datatype.
        data2 (str):         Password or none, depending on datatype.
        expires (float):     Expiration date of the data.
        data_type (DataType) Which DataType to prepare.
    
    Returns:
        str:    Formated json string with key-value pairs of the data.
    """

    if data_type is DataType.DATATYPE_USER_INFO:
        data = f'{"{"}\n' + \
               f'   "{data_keys[data_type][0]}": "{data1}",\n' + \
               f'   "{data_keys[data_type][1]}": "{data2}",\n' + \
               f'   "expires": "{expires}"\n' + \
               f'{"}"}'    
    else:
        data = f'{"{"}\n' + \
               f'   "{data_keys[data_type][0]}": "{data1}",\n' + \
               f'   "expires": "{expires}"\n' + \
               f'{"}"}'

    return data
