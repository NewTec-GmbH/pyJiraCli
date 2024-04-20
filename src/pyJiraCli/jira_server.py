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

from jira import JIRA, exceptions

from pyJiraCli import crypto_file_handler as crypto
from pyJiraCli.retval import Ret

################################################################################
# Variables
################################################################################
DEFAULT_SERVER = "https://jira.newtec.zz"

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################
def login(user, pw):
    """ login to jira server with user info or user info from file
        
        param:
        user: provided username from the commandline or None
        pw: provided password from the commandline or None
        
        return:
        jira obj or None if no succesful login
        the exit code of the module
    """

    server_url = _get_server_url()

    if user is None or pw is None:
        # get login information from login module
        user, token, ret_status = crypto.decrypt_information(crypto.DataType.DATATYPE_TOKEN_INFO)

        if ret_status == Ret.RET_OK:
            return _login_with_token(token, server_url)

        user, pw, ret_status = crypto.decrypt_information(crypto.DataType.DATATYPE_USER_INFO)

        if ret_status == Ret.RET_OK:
            return _login_with_password(user, pw, server_url)

        return None, ret_status

def try_login(user, pw, token):
    """ try login with jira lib
        dont return jira obj only return OK if login succesful
        
        param:
        user: username or email
        pw: password for login
        token: API Token for authentification
        
        return:
        the exit status of the module
    """

    server_url = _get_server_url()

    if token is None:
        obj, ret_status = _login_with_password(user, pw, server_url)

    elif pw is None:
        obj, ret_status = _login_with_token(token, server_url)

    else:
        return Ret.RET_ERROR_MISSING_LOGIN_INFO

    if obj is None:
        return Ret.RET_ERROR_JIRA_LOGIN

    return ret_status

def _login_with_token(token, url):
    os.environ["SSL_CERT_FILE"] = certifi.where()

    try:
        jira = JIRA(server=url, token_auth=token, options={"verify": False})
        jira.verify_ssl = False

        return jira, Ret.RET_OK

    except exceptions.JIRAError as e:
        #print error
        print(e)
        return None, Ret.RET_ERROR_JIRA_LOGIN

def _login_with_password(user, pw, url):
    os.environ["SSL_CERT_FILE"] = certifi.where()

    try:
        jira = JIRA(server=url, basic_auth=(user, pw), options={"verify": False})
        jira.verify_ssl = False

        return jira, Ret.RET_OK

    except exceptions.JIRAError as e:
        #print error
        print(e)
        return None, Ret.RET_ERROR_JIRA_LOGIN


def _get_server_url():

    server_url, data2_, ret_status = crypto.decrypt_information(crypto.DataType.DATATYPE_SERVER)

    if ret_status != Ret.RET_OK:
        server_url, data2_, ret_status = \
            crypto.decrypt_information(crypto.DataType.DATATYPE_SERVER_DEFAULT)

        if ret_status != Ret.RET_OK:
            server_url = DEFAULT_SERVER

    return server_url
