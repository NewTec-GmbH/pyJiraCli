"""Jira server connection module"""

# BSD 3-Clause License
#
# Copyright (c) 2024 - 2025, NewTec GmbH
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
import sys
from typing import Optional

import certifi
import urllib3

from jira import JIRA, exceptions
from requests import exceptions as reqex
from urllib3 import exceptions as urlex

from pyProfileMgr.profile_mgr import ProfileMgr

from pyJiraCli.printer import Printer, PrintType
from pyJiraCli.ret import Ret, Warnings

# pylint: disable=E0401
if os.name == 'nt':
    import msvcrt
else:
    import tty
    import termios
# pylint: enable=E0401

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################


class Server:
    """This class handles connection to the Jira server.

    Args:
        timeout (float): The timeout for the requests in seconds. Default is 10 seconds.
        Shorter timeout can result in failed requests,
        depending on the speed of the server and the size of the request.
    """

    def __init__(self, timeout: float = 10):
        self._jira_obj = None
        self._search_result = None
        self._cert_path = None
        self._server_url = None
        self._user = None
        self._max_retries = 0
        self._timeout = timeout

        urllib3.disable_warnings()

    # pylint: disable=R0913,R0917
    def login(self,
              arg_profile_name: Optional[str],
              arg_server_url: Optional[str],
              arg_token: Optional[str],
              arg_username: Optional[str],
              arg_password: Optional[str]) -> Ret.CODE:
        """ Login to Jira server with user info or login info from
            stored token or user file.

        Args:
            arg_profile_name (str): The server profile that shall be used.
            arg_server_url (str): The URL of the server to log in to.
            arg_token (str): The API token used for authentication.
            arg_username (str): The username for authentication.
            arg_password (str): The password for authentication.

        returns:
            Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
        """
        ret_status = Ret.CODE.RET_OK
        _printer = Printer()

        # Login using settings from profile
        if arg_profile_name is not None:
            ret_status = self._login_using_profile(arg_profile_name)

        # Else login with command line parameters
        elif arg_server_url is not None:

            ret_status = self._login_using_direct_args(
                arg_server_url, arg_token, arg_username, arg_password)

        else:
            # Neither profile nor command line information given
            ret_status = Ret.CODE.RET_ERROR
            print("Missing server URL to connect to.")
            _printer.print_error(
                PrintType.ERROR, Ret.CODE.RET_ERROR_JIRA_LOGIN)

        if Ret.CODE.RET_OK == ret_status:
            if self._user is not None:
                _printer.print_info(
                    'Login successful. Logged in as: ', self._user)
            else:
                _printer.print_info('Login successful.')

        return ret_status

    def get_handle(self) -> JIRA:
        """ Return the handle to the jira rest api.

        Returns:
           JIRA: The jira object.
        """
        return self._jira_obj

    def search(self, search_str: str, max_results: int, fields: list[str]) -> Ret.CODE:
        """ Search for jira issues with a search string.
            The maximum of found issues can be set.

        Args:
            search_str (str): The string by which to search issues for.
            max_results (int): The maximum number of search results.
            fields (list[str]): The fields to search for in the work items.

        Returns:
            Ret.CODE:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
        """

        ret_status = Ret.CODE.RET_OK

        if self._jira_obj is None:
            ret_status = Ret.CODE.RET_ERROR

        else:
            try:
                self._search_result = self._jira_obj.search_issues(search_str,
                                                                   maxResults=max_results,
                                                                   fields=fields)

            except exceptions.JIRAError as e:
                print(e.text)
                ret_status = Ret.CODE.RET_ERROR_INVALID_SEARCH

        return ret_status

    def get_search_result(self) -> list:
        """ Return the results from a
            successful search.

        Returns:
            list: A list with all the found issues from the last search.
        """
        return self._search_result

    def _login_using_profile(self, profile_name: str) -> Ret.CODE:
        ''' Login to Jira server using the profile settings.'''
        _printer = Printer()
        _profile_mgr = ProfileMgr()

        ret_status = _profile_mgr.load(profile_name)

        if ret_status == Ret.CODE.RET_OK:
            self._cert_path = _profile_mgr.loaded_profile.cert_path
            self._server_url = _profile_mgr.loaded_profile.server_url
            api_token = _profile_mgr.loaded_profile.token

            _printer.print_info('Logging in to Jira server:', self._server_url)

            if self._cert_path is None:
                _printer.print_error(
                    PrintType.WARNING, Warnings.CODE.WARNING_UNSAVE_CONNECTION)

            # Use token (preferred)
            if api_token is not None:
                _printer.print_info('Using token for login.')

                ret_status = self._login_with_token(api_token)
            # Else user/password
            else:
                _printer.print_info('Using user/password for login.')

                self._user = _profile_mgr.loaded_profile.user
                password = _profile_mgr.loaded_profile.password

                ret_status = self._login_with_password(self._user, password)

        return ret_status

    def _login_using_direct_args(self, server_url: str,
                              token: str, username: str, password: str) -> Ret.CODE:
        ''' Login to Jira server using the command line arguments directly. '''
        self._server_url = server_url

        _printer = Printer()
        ret_status = Ret.CODE.RET_OK

        if self._cert_path is None:
            _printer.print_error(
                PrintType.WARNING, Warnings.CODE.WARNING_UNSAVE_CONNECTION)

        _printer.print_info('Login in to:', self._server_url)

        if token is not None:
            # Login with token
            ret_status = self._login_with_token(token)
        elif (username is not None) and (password is not None):
            # Login with user and password
            ret_status = self._login_with_password(
                username, password)
        else:
            # No credentials given
            ret_status = Ret.CODE.RET_ERROR
            print("Missing credentials (token or user/password) to login.")
            _printer.print_error(
                PrintType.ERROR, Ret.CODE.RET_ERROR_JIRA_LOGIN)

        return ret_status

    def _login_with_token(self, token: str) -> Ret.CODE:
        """ Login to jira with API token.

        Args:
            token (str):    The API token for login.

        Returns:
            Ret.CODE:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
        """

        user = None
        ret_status = Ret.CODE.RET_OK

        os.environ["SSL_CERT_FILE"] = certifi.where()

        try:
            if self._cert_path is None:
                self._jira_obj = JIRA(server=self._server_url,
                                      options={'verify': False},
                                      token_auth=token,
                                      max_retries=self._max_retries,
                                      timeout=self._timeout)
            else:
                self._jira_obj = JIRA(server=self._server_url,
                                      options={'verify': self._cert_path},
                                      token_auth=token,
                                      max_retries=self._max_retries,
                                      timeout=self._timeout)

            user = self._jira_obj.current_user()

            self._jira_obj.verify_ssl = False

        except (exceptions.JIRAError,
                urlex.MaxRetryError,
                reqex.ConnectionError,
                reqex.MissingSchema,
                reqex.InvalidSchema,
                reqex.InvalidURL) as e:
            # print error
            ret_status = Ret.CODE.RET_ERROR_JIRA_LOGIN

            if isinstance(e, exceptions.JIRAError):
                print(e.text)

            elif isinstance(e, (reqex.InvalidSchema,
                                reqex.MissingSchema,
                                reqex.InvalidURL)):
                ret_status = Ret.CODE.RET_ERROR_INVALID_URL

            else:
                print(str(e))

        if user is None:
            ret_status = Ret.CODE.RET_ERROR_JIRA_LOGIN

        self._user = user

        return ret_status

    def _login_with_password(self, user: str, pw: str) -> Ret.CODE:
        """ Login to jira with username and password.

        Args:
            user (str):     Username for login.
            pw (str):       Password for login.

        Returns:
            Ret.CODE:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
        """

        ret_status = Ret.CODE.RET_OK

        os.environ["SSL_CERT_FILE"] = certifi.where()

        try:
            if self._cert_path is None:
                self._jira_obj = JIRA(server=self._server_url,
                                      basic_auth=(user, pw),
                                      options={'verify': False},
                                      max_retries=self._max_retries,
                                      timeout=self._timeout)
            else:
                self._jira_obj = JIRA(server=self._server_url,
                                      basic_auth=(user, pw),
                                      options={'verify': self._cert_path},
                                      max_retries=self._max_retries,
                                      timeout=self._timeout)

            user = self._jira_obj.current_user()

            self._jira_obj.verify_ssl = False

        except (exceptions.JIRAError,
                urlex.MaxRetryError,
                reqex.ConnectionError,
                reqex.MissingSchema,
                reqex.InvalidSchema,
                reqex.InvalidURL) as e:
            # print error
            ret_status = Ret.CODE.RET_ERROR_JIRA_LOGIN

            if isinstance(e, exceptions.JIRAError):
                print(e.text)

            elif isinstance(e, (reqex.InvalidSchema,
                                reqex.MissingSchema,
                                reqex.InvalidURL)):
                ret_status = Ret.CODE.RET_ERROR_INVALID_URL

            else:
                print(str(e))

        self._user = user

        return ret_status

################################################################################
# Functions
################################################################################


def _get_user_credentials() -> tuple[str, str]:
    """Prompt the user to enter a username and a password.
    The password input is masked with '*' characters.

    Returns:
        tuple[str, str]: A tuple containing the username and the password.
    """
    username = input("Enter your username: ")

    print("Enter your password: ", end="", flush=True)
    password = _get_password()
    print('\r', end='')

    return username, password


if os.name == 'nt':
    def _get_password() -> str:
        """Prompt the user to enter a password with '*' masking for Windows.

        Returns:
            str: The entered password.
        """

        password = ""
        while True:
            char = msvcrt.getch()
            if char in {b'\n', b'\r'}:
                break

            if char == b'\x08':  # Backspace
                if len(password) > 0:
                    password = password[:-1]
                    sys.stdout.write('\b \b')
            else:
                password += char.decode('utf-8')
                sys.stdout.write('*')
            sys.stdout.flush()
        print()
        return password

else:
    def _get_password() -> str:
        """Prompt the user to enter a password with '*' masking for Unix-based systems.

        Returns:
            str: The entered password.
        """

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            password = ""
            while True:
                char = sys.stdin.read(1)
                if char in ('\n', '\r'):
                    break

                if char == '\b' or ord(char) == 127:
                    if len(password) > 0:
                        password = password[:-1]
                        sys.stdout.write('\b \b')
                else:
                    password += char
                    sys.stdout.write('*')
                sys.stdout.flush()
            print()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return password
