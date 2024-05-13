"""jira server connection module"""

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
import certifi
import urllib3

from jira import JIRA, exceptions
from requests import exceptions as reqex
from urllib3 import exceptions as urlex

from pyJiraCli.crypto_file_handler import Crypto, DataType, DataMembers
from pyJiraCli.error_handler import Error, ErrorType
from pyJiraCli.ret import Ret, Warnings

################################################################################
# Variables
################################################################################
DEFAULT_SERVER = "https://jira.newtec.zz"

################################################################################
# Classes
################################################################################
class Server:
    """This class handles connection to the jira server.
    """
    def __init__(self):
        self._crypto_h = Crypto()
        self._error_h = Error()
        self._server_url = DEFAULT_SERVER
        self._jira_obj = None
        self._search_result = None
        self._cert_path = None
        self._user = None

        urllib3.disable_warnings()

    def logout(self) -> None:
        """ Logout from the jira session and delete all tmp files.
        """
        self._crypto_h.delete_cert_path()

    def login(self, user:str, pw:str) -> Ret:
        """ Login to jira server with user info or login info from 
            stored token or user file.

        Args:
            user (str):     Provided username from the commandline or None.
            pw (str):       Provided password from the commandline or None.

        returns:
            Ret:   Returns Ret.RET_OK if succesfull or the corresponding error code if not.
        """
        ret_status = Ret.RET_OK
        cert_path = self._crypto_h.get_cert_path()

        self._get_server_url()

        if cert_path is None:
            self._error_h.print(ErrorType.WARNING, Warnings.WARNING_UNSAVE_CONNECTION)

        else:
            self._cert_path = cert_path

        if user is None or pw is None:
            # get login information from login module
            ret_status = self._crypto_h.decrypt_information(DataType.DATATYPE_TOKEN_INFO)

            if ret_status == Ret.RET_OK:
                token = self._crypto_h.get_data(DataMembers.DATA_MEM_1)

                ret_status = self._login_with_token(token)

            else:
                ret_status = self._crypto_h.decrypt_information(DataType.DATATYPE_USER_INFO)

                if ret_status == Ret.RET_OK:
                    user = self._crypto_h.get_data(DataMembers.DATA_MEM_1)
                    pw = self._crypto_h.get_data(DataMembers.DATA_MEM_2)
                    ret_status = self._login_with_password(user, pw)

        else:
            ret_status = self._login_with_password(user, pw)

        if ret_status == Ret.RET_OK and \
           self._user is not None:
            self._error_h.print_info('Login succesful. Logged in as:', self._user)

        return ret_status

    def try_login(self, user:str=None, pw:str=None, token:str=None) -> Ret:
        """ Try to login to jira.
            Dont return the jira obj, only return OK if the login 
            was succesful.

        Args:
            user (str):     Username or email for login or None.
            pw (str):       Password for login or None.
            token (str):    API Token for authentification or None.

        Returns:
            Ret:   Returns Ret.RET_OK if succesfull or the corresponding error code if not.
        """

        ret_status = Ret.RET_OK
        cert_path = self._crypto_h.get_cert_path()

        self._get_server_url()

        if cert_path is None:
            self._error_h.print(ErrorType.WARNING, Warnings.WARNING_UNSAVE_CONNECTION)

        else:
            self._cert_path = cert_path

        if token is None:
            ret_status = self._login_with_password(user, pw)

        elif pw is None:
            ret_status = self._login_with_token(token)

        else:
            return Ret.RET_ERROR

        if ret_status == Ret.RET_OK and \
           self._user is not None:
            self._error_h.print_info('Login succesful. Logged in as:', self._user)

        self._crypto_h.delete_cert_path()

        return ret_status

    def get_handle(self) -> object:
        """ Return the handle to the jira rest api.

        Returns:
           obj: The jira object.
        """
        return self._jira_obj

    def search(self, search_str:str, max_results:int) -> Ret:
        """_summary_

        Args:
            search_str (str): _description_
            max_results (int): _description_

        Returns:
            Ret: _description_
        """

        ret_status = Ret.RET_OK

        if self._jira_obj is None:
            ret_status = Ret.RET_ERROR

        else:
            try:
                self._search_result = self._jira_obj.search_issues(search_str,
                                                                   maxResults=max_results)

            except exceptions.JIRAError as e:
                print(e.text)
                ret_status = Ret.RET_ERROR_INVALID_SEARCH

        return ret_status

    def get_search_result(self) -> list:
        """_summary_

        Returns:
            list: _description_
        """
        return self._search_result

    def _login_with_token(self, token:str) -> Ret:
        """ Login to jira with API token.

        Args:
            token (str):    The API token for login.

        Returns:
            Ret:   Returns Ret.RET_OK if succesfull or the corresponding error code if not.
        """

        user = None
        ret_status = Ret.RET_OK

        os.environ["SSL_CERT_FILE"] = certifi.where()

        try:
            if self._cert_path is None:
                self._jira_obj = JIRA(server= self._server_url, #'https://jira-dev.newtec.zz:8443',
                                      options={'verify' : False},
                                      token_auth=token)
            else:
                self._jira_obj = JIRA(server=self._server_url,
                                      options={'verify' : self._cert_path},
                                      token_auth=token)

            user = self._jira_obj.current_user()

            self._jira_obj.verify_ssl = False

        except (exceptions.JIRAError, reqex.ConnectionError, urlex.MaxRetryError) as e:
            #print error
            if isinstance(e, exceptions.JIRAError):
                print(e.text)
            else:
                print(str(e))

            ret_status = Ret.RET_ERROR_JIRA_LOGIN

        if user is None:
            ret_status = Ret.RET_ERROR_JIRA_LOGIN

        self._user = user

        return ret_status

    def _login_with_password(self, user:str, pw:str) -> Ret:
        """ Login to jira with username and password.

        Args:
            user (str):     Username for login.
            pw (str):       Password for login.

        Returns:
            Ret:   Returns Ret.RET_OK if succesfull or the corresponding error code if not.
        """

        ret_status = Ret.RET_OK

        os.environ["SSL_CERT_FILE"] = certifi.where()

        try:
            if self._cert_path is None:
                self._jira_obj = JIRA(server=self._server_url,
                                      basic_auth=(user, pw))
            else:
                self._jira_obj = JIRA(server=self._server_url,
                                      basic_auth=(user, pw),
                                      options={'verify' : self._cert_path})

            user = self._jira_obj.current_user()

            self._jira_obj.verify_ssl = False

        except (exceptions.JIRAError, reqex.ConnectionError, urlex.MaxRetryError) as e:
            #print error
            if isinstance(e, exceptions.JIRAError):
                print(e.text)
            else:
                print(str(e))

            ret_status = Ret.RET_ERROR_JIRA_LOGIN

        if user is None:
            ret_status = Ret.RET_ERROR_JIRA_LOGIN

        self._user = user

        return ret_status

    def _get_server_url(self) -> str:
        """ Get the server url from the encrypted files.
            If no server data is available a hardcoded default server
            will be returned.

        Returns:
            str: The server url.
        """
        data_type = DataType.DATATYPE_SERVER
        ret_status = self._crypto_h.decrypt_information(data_type)

        if ret_status is not Ret.RET_OK:
            data_type = DataType.DATATYPE_SERVER_DEFAULT
            ret_status = self._crypto_h.decrypt_information(data_type)

            if ret_status is not Ret.RET_OK:
                server_url = DEFAULT_SERVER

                self._error_h.print(ErrorType.WARNING, Warnings.WARNING_SERVER_URL_MISSING)
                self._error_h.print_info(f"Using hardcoded default url at {DEFAULT_SERVER}")

        if ret_status is Ret.RET_OK:
            server_url = self._crypto_h.get_data(DataMembers.DATA_MEM_1)

        self._server_url = server_url

################################################################################
# Functions
################################################################################
