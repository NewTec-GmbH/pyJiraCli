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
PATH_TO_PROFILE_FOLDER   = "/.pyJiraCli/.profiles/"
CERT_FILE = ".cert.crt"
DATA_FILE = ".data.json"

URL_KEY = 'url'
TOKEN_KEY = 'token'

FILE_ATTRIBUTE_HIDDEN = 0x02
################################################################################
# Classes
################################################################################
class ProfileHandler:
    """ The ProfileHandler class handles all 
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
            cert_path:str) -> Ret.CODE:
        """ Adds a new profile with the provided details.

        Args:
            profile_name (str): The unique name of the profile.
            profile_url (str): The URL associated with the profile.
            login_token (str): The login token for profile authentication.
            cert_path (str): The file path to the profile's server certificate.

        Returns:
            Ret.CODE: A status code indicating the result of the operation.
        """

        ret_status = Ret.CODE.RET_OK
        _printer = Printer()
        add_profile = True

        write_dict = {
            URL_KEY : profile_url
            }

        if login_token is None:
            _printer.print_error(PrintType.WARNING, Warnings.CODE.WARNING_TOKEN_RECOMMENDED)
        else:
            write_dict[TOKEN_KEY] = login_token

        profile_path = _get_path_to_login_folder() + f"{profile_name}/"

        if not os.path.exists(profile_path):
            os.mkdir(profile_path)
        else:
            print("A profile with this name already exists. Do you want to override this profile?")
            response = input("(y/n): ")

            if response == 'y':
                if os.path.exists(profile_path + DATA_FILE):
                    os.remove(profile_path + DATA_FILE)

                if os.path.exists(profile_path + CERT_FILE):
                    os.remove(profile_path + CERT_FILE)
            else:
                add_profile = False

        if add_profile:
            ret_status = _add_new_profile(write_dict, profile_path, cert_path)

            if ret_status == Ret.CODE.RET_OK:
                _printer.print_info("A new profile was successfully created. Profile name:",
                                    profile_name)

        else:
            _printer.print_info("Adding profile canceled.")

        return ret_status

    def add_certificate(self, profile_name:str, cert_path:str) -> Ret.CODE:
        """ Adds a server certificate to the specified profile.

        Args:
            profile_name (str): The name of the profile.
            cert_path (str): The file path to the certificate.

        Returns:
            Ret.CODE: A status code indicating the result of the operation.
        """
        ret_status = Ret.CODE.RET_OK

        _file = File()
        _printer = Printer()
        profile_path = _get_path_to_login_folder() + f"{profile_name}/"

        if os.path.exists(cert_path):
            ret_status =_file.set_filepath(cert_path)
        else:
            ret_status = Ret.CODE.RET_ERROR_FILEPATH_INVALID

        if ret_status == Ret.CODE.RET_OK:
            ret_status = _file.read_file()

        if ret_status == Ret.CODE.RET_OK:
            cert_data = _file.get_file_content()
            ret_status =_file.set_filepath(profile_path + CERT_FILE)

        if ret_status == Ret.CODE.RET_OK:
            if os.path.exists(profile_path + CERT_FILE):
                os.remove(profile_path + CERT_FILE)

            _file.write_file(cert_data)
            _file.hide_file()

            _printer.print_info("Successfully added a certificate to profile:",
                               profile_name)

        return ret_status

    def add_token(self, profile_name:str, api_token:str) -> Ret.CODE:
        """ Adds an API token to the specified profile.

        Args:
            profile_name (str): The name of the profile.
            api_token (str): The API token for accessing the profile.

        Returns:
            Ret.CODE: A status code indicating the result of the operation.
        """
        ret_status = Ret.CODE.RET_OK

        _file = File()
        _printer = Printer()
        profile_path = _get_path_to_login_folder() + f"{profile_name}/"

        self.load(profile_name)

        write_dict = {
            URL_KEY   : self._profile_url,
            TOKEN_KEY : api_token
        }

        os.remove(profile_path + DATA_FILE)

        profile_data = json.dumps(write_dict, indent=4)

        ret_status =_file.set_filepath(profile_path + DATA_FILE)

        if ret_status == Ret.CODE.RET_OK:
            _file.write_file(profile_data)
            _file.hide_file()

            _printer.print_info("Added an API token to profile:", profile_name)

        return ret_status

    def add_config(self, issue_config_file:str, project_config_file:str) -> Ret.CODE:
        """ Adds configuration settings from specified files to the profile.

        Args:
            issue_config_file (str): Path to the file containing issue configuration settings.
            project_config_file (str): Path to the file containing project configuration settings.

        Returns:
            Ret.CODE: Status code indicating success or failure of the configuration addition.
        """
        ret_status = Ret.CODE.RET_OK

        # pseudo code to remove unused-argument error
        # until the function is implemented properly
        print(f"{issue_config_file}, {project_config_file}")

        return ret_status

    def load(self, profile_name:str) -> Ret.CODE:
        """ Loads the server profile information 
            for the specified profile.

        Args:
            profile_name (str): Name of the server profile to load.

        Returns:
            Ret.CODE: Status code indicating the success or failure of the load operation.
        """
        ret_status = Ret.CODE.RET_OK

        _file = File()

        profile_path = _get_path_to_login_folder() + f"{profile_name}/"

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
        """ This function will format and return all
            available config data so that it can
            be used by the other modules.

        Returns:
            dict: A dictionary containing all formatted configuration data.
        """
        config_dict = {}

        # code goes here

        return config_dict

    def delete(self, profile_name:str) -> None:
        """_summary_

        Args:
            profile_name (str): _description_
        """
        _printer = Printer()
        profile_path = _get_path_to_login_folder() + f"{profile_name}/"

        if os.path.exists(profile_path):
            os.remove(profile_path + DATA_FILE)

            if os.path.exists(profile_path + CERT_FILE):
                os.remove(profile_path + CERT_FILE)

            os.rmdir(profile_path)

            _printer.print_info("Successfully removed profile:", profile_name)

        else:
            _printer.print_info("Can't delete profile:", profile_name,
                               "A profile with this name does not exist.")

    def get_cert_path(self) -> str:
        """ Retrieves the file path to the server certificate.

        Returns:
            str: The file path of the server certificate used by the profile.
        """
        return self._profile_cert

    def get_server_url(self) -> str:
        """ Retrieves the server URL associated with the profile.

        Returns:
            str: The server URL used by the profile.
        """
        return self._profile_url

    def get_api_token(self) -> str:
        """ Retrieves the API token associated with the profile.

        Returns:
            str: The API token used by the profile for authentication.
        """
        return self._profile_token

################################################################################
# Functions
################################################################################
def _add_new_profile(write_dict:dict, profile_path:str, cert_path:str) -> Ret.CODE:
    """ Adds a new server profile to the configuration.

    Args:
        write_dict (dict): Dictionary containing profile data to be written.
        profile_path (str): Path where the profile data will be saved.
        cert_path (str): Path to the server certificate associated with the profile.

    Returns:
        Ret.CODE: Status code indicating the success or failure of the profile addition.
    """
    ret_status = Ret.CODE.RET_OK
    _file = File()
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

    return ret_status

def _get_path_to_login_folder() -> str:
    """ Returns the path to the pyJiraCli tool data.
        All tool data (profile/configs) is stored in the users
        home directory.
    
    Returns:
        str: The path to the login data folder.
    """

    user_info_path = os.path.expanduser("~") + PATH_TO_PROFILE_FOLDER

    if not os.path.exists(user_info_path):

        os.makedirs(user_info_path)

        if os.name == 'nt':
            ctypes.windll.kernel32.SetFileAttributesW(user_info_path,
                                                      FILE_ATTRIBUTE_HIDDEN)

    return user_info_path
