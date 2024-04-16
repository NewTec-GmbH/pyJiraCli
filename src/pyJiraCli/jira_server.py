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

from jira import JIRA

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
    """"login to jira server with user info or user info from file"""

    if user is None and pw is None:
        # get login information from login module
        user, pw, ret_status = crypto.decrypt_user_information()

        if ret_status != Ret.RET_OK:
            return ret_status

    server_url, ret_status = crypto.decrypt_server_information()

    if ret_status != Ret.RET_OK:
        server_url = DEFAULT_SERVER

    os.environ["SSL_CERT_FILE"] = certifi.where()

    try:
        jira = JIRA(server=server_url, basic_auth=(user, pw), options={"verify": False})
        jira.verify_ssl = False

        return jira, Ret.RET_OK

    except jira.exceptions.JIRAError as e:
        #print error
        print(e)
        return None, Ret.RET_ERROR_JIRA_LOGIN
