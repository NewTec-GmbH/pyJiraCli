"""Command to store login information
   Stores User, pw and a server url in an encoded file
   or deltes stored login informations"""
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
from pyJiraCli import crypto_file_handler as crypto
from pyJiraCli import jira_server as server
from pyJiraCli.retval import Ret
################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################
# subparser for the 'set_login' command
def add_parser(subparser):
    """register subparser commands for the set_login module"""
    sb_login = subparser.add_parser('login', help="save or delete login information")

    sb_login.add_argument('-user', type=str, metavar='<username>', help="jira username for login")
    sb_login.add_argument('-pw', type=str, metavar='<password>', help="jira password for login")
    sb_login.add_argument('-url', type=str, metavar='<server url>', help="jira server for login")
    sb_login.add_argument('-delete', action='store_true', help="delete login information")
    sb_login.add_argument('--userinfo', '-ui', action='store_true',
                           help="delete user infomation only")
    sb_login.add_argument('--server', '-s', action='store_true',
                           help="delete server information only")
    sb_login.set_defaults(func=cmd_login)

######################################################
## set_login command function                       ##
######################################################
def cmd_login(args):
    """"store or delete login information"""    
    if args.delete:
        return _delete_login_file(args)

    else:
        return _store_login_info(args)
######################################################
def _store_login_info(args):

    ret_status = Ret.RET_OK

    if args.user is None and args.pw is None and args.url is None:
        return Ret.RET_ERROR_MISSING_LOGIN_INFO

    if args.user is not None or args.pw is not None:
        if args.pw is None or args.user is None:
            return Ret.RET_ERROR_MISSING_UNSERINFO

        jira, ret_status = server.login(args.user, args.pw)

        if ret_status != Ret.RET_OK:
            return ret_status

        ret_status = crypto.encrypt_user_information(args.user, args.pw)

    if args.url is not None:
        ret_status = crypto.encrypt_server_information(args.url)

    return ret_status

def _delete_login_file(args):

    if args.userinfo:
        crypto.delete_user_information()

    if args.server:
        crypto.delete_server_information()

    if not args.userinfo and not args.server:
        crypto.delete_user_information()
        crypto.delete_server_information()

    return Ret.RET_OK
