""" The Profile class.
    Handles adding, deleting or changimg server
    profiles.
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
import ctypes

import json

from pyJiraCli.file_handler import FileHandler as File
from pyJiraCli.ret import Ret, Warnings
from pyJiraCli.printer import Printer, PrintType
################################################################################
# Variables
################################################################################
PATH_TO_PROFILE_FOLDER   = "\\.pyJiraCli\\.profiles\\"
CERT_FILE = ".cert.crt"
DATA_FILE = ".data.json"

URL_KEY = 'url'
TOKEN_KEY = 'token'

FILE_ATTRIBUTE_HIDDEN = 0x02
################################################################################
# Classes
################################################################################
class Profile:
    """ The profile class handles all 
        processes regarding server profiles.
        This includes adding, deleting or configuring
        Profile data. 
    """
    def __init__(self):
        self._profile_name = None
        self._profile_url = None
        self._profile_token = None
        self._profile_cert = None
        self._profile_config = None

    def add(self,
            profile_name:str,
            profile_url:str,
            login_token:str,
            cert_path:str) -> Ret:
        """_summary_

        Args:
            profile_name (str): _description_
            profile_url (str): _description_
            login_token (str): _description_

        Returns:
            Ret: _description_
        """

        ret_status = Ret.CODE.RET_OK
        _printer = Printer()
        _file = File()

        write_dict = {
            URL_KEY : profile_url,
            }

        if login_token is None:
            _printer.print_error(PrintType.WARNING, Warnings.CODE.WARNING_TOKEN_RECOMMENDED)
        else:
            write_dict[TOKEN_KEY] = login_token

        profile_path = _get_path_to_login_folder() + f"{profile_name}\\"

        cont = True

        if not os.path.exists(profile_path):
            os.mkdir(profile_path)
        else:
            print("A profile with this name already exists. Do you want to overide this profile?")
            response = input("(y/n): ")

            if response == 'y':
                os.remove(profile_path + DATA_FILE)

                if os.path.exists(profile_path + CERT_FILE):
                    os.remove(profile_path + CERT_FILE)
            else:
                cont = False

        if cont:
            profile_data = json.dumps(write_dict, indent=4)

            ret_status =_file.set_filepath(profile_path + DATA_FILE)

            if ret_status == Ret.CODE.RET_OK:
                _file.write_file(profile_data)
                _file.hide_file()

            if cert_path is not None and \
               os.path.exists(cert_path):
                ret_status =_file.set_filepath(cert_path)

                if ret_status == Ret.CODE.RET_OK:
                    ret_status = _file.read_file()

                if ret_status == Ret.CODE.RET_OK:
                    cert_data = _file.get_file_content()

                ret_status =_file.set_filepath(profile_path + CERT_FILE)

                if ret_status == Ret.CODE.RET_OK:
                    _file.write_file(cert_data)
                    _file.hide_file()
        else:
            _printer.print_info("Adding profile canceled.")

        return ret_status

    def add_certificate(self, profile_name:str, cert_path:str) -> Ret:
        """_summary_

        Args:
            cert_path (str): _description_

        Returns:
            Ret: _description_
        """
        pass

    def add_config(self, issue_config_file:str, project_config_file:str) -> Ret:
        """_summary_

        Args:
            issue_config_file (str): _description_
            project_config_file (str): _description_

        Returns:
            Ret: _description_
        """
        pass

    def load(self, profile_name:str) -> Ret:
        """_summary_

        Args:
            profile_name (str): _description_

        Returns:
            Ret: _description_
        """
        ret_status = Ret.CODE.RET_OK

        _file = File()

        profile_path = _get_path_to_login_folder() + f"{profile_name}\\"

        if os.path.exists(profile_path):
            ret_status = _file.set_filepath(profile_path + DATA_FILE)

            if ret_status == Ret.CODE.RET_OK:
                _file.open_file('r')
                profile_dict = json.load(_file.get_file())

                self._profile_url = profile_dict[URL_KEY]

                if TOKEN_KEY in profile_dict:
                    self._profile_token = profile_dict[TOKEN_KEY]

                if os.path.exists(profile_path + CERT_FILE):
                    self._profile_cert = profile_path + CERT_FILE
        else:
            ret_status = Ret.CODE.RET_ERROR_PROFILE_NOT_FOUND

        return ret_status

    def get_config_data(self) -> dict:
        """ This function will format all
            available config data so that it can
            be used by the other modules.

        Returns:
            dict: _description_
        """
        pass

    def delete(self, profile_name:str) -> None:
        """_summary_

        Args:
            profile_name (str): _description_
        """
        pass

    def get_cert_path(self) -> str:
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._profile_cert

    def get_server_url(self) -> str:
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._profile_url

    def get_api_token(self) -> str:
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._profile_token

################################################################################
# Functions
################################################################################
def _get_path_to_login_folder() -> str:
    """ Returns the path to the pyJiraCli tool data.
        All tool data (logindata/configs) is stored in the users
        home directory.
    
    Returns:
        str: The path to the login data folder.
    """

    user_info_path = os.path.expanduser("~") + PATH_TO_PROFILE_FOLDER

    if not os.path.exists(user_info_path):
        os.makedirs(user_info_path)
        ctypes.windll.kernel32.SetFileAttributesW(user_info_path,
                                                  FILE_ATTRIBUTE_HIDDEN)
    return user_info_path
