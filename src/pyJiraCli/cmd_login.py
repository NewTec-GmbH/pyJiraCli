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
import time

from pyJiraCli import crypto_file_handler as crypto
from pyJiraCli import jira_server as server
from pyJiraCli.retval import Ret

################################################################################
# Variables
################################################################################
# 2 months in seconds
DEFAULT_EXPIRATION_TIME = 2 * 30 * 24 * 60 * 60
################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################
# subparser for the 'set_login' command
def register(subparser):
    """ register subparser commands for the login module
        
        Args:
        subparser   the command subparser provided via __main__.py
        
        Returns:
        sb_login    the commmand parser of this module
    """

    sb_login = subparser.add_parser('login',
                                     help="save or delete login information")

    sb_login.add_argument('-token',
                           type=str,
                           metavar='<API token>',
                           help="user API token for login authenfication")

    sb_login.add_argument('-url',
                           type=str,
                           metavar='<server url>',
                           help="jira server for login")

    sb_login.add_argument('-expires',
                           type=int,
                           metavar='<time>',
                           help="time after which the stored login info \
                                 will expire. default = 30 days")

    sb_login.add_argument('--min',
                           action='store_true',
                           help="expire time in minutes")

    sb_login.add_argument('--day',
                           action='store_true',
                           help="expire time in days")

    sb_login.add_argument('--month',
                           action='store_true',
                           help="expire time in months")

    sb_login.add_argument('-delete',
                           action='store_true',
                           help="delete login information")

    sb_login.add_argument('--default',
                           action='store_true',
                           help="delete or store default server url")

    sb_login.add_argument('--userinfo',
                          '-ui',
                           action='store_true',
                           help="delete user infomation only")

    sb_login.add_argument('--server',
                          '-s',
                           action='store_true',
                           help="delete server information only")

    sb_login.add_argument('--token',
                          '-t',
                           action='store_true',
                           help="delete API token information only")


    return sb_login

def execute(args):
    """ execute command function
    
        Args: 
        args        the command line arguments
        
        Returns:
        retval.Ret  the exit status of the _cmd_login function
    """
    return _cmd_login(args)

def _cmd_login(args):
    """" store or delete login information
        
         Args:
         args           the command line arguments
        
         Returns:
         ret_status     the return status of the module
    """
    ret_status = Ret.RET_OK

    if args.delete:
        ret_status =  _delete_login_file(args.userinfo, args.token, args.server, args.default)

    ret_status = _store_login_info(args)

    return ret_status

def _store_login_info(args):
    """ save the login info in a encrypted file
        userinfo(user, pw), token, server and default server
        are all a saved in seperate files
        
        param:
        args: commnd line arguments

        return:
        teh status of teh module
    """
    ret_status = Ret.RET_OK

    user = args.user
    pw = args.pw
    url = args.url
    token = args.token
    expiration = args.expires

    if token is None and pw is None and url is None:
        return Ret.RET_ERROR_MISSING_LOGIN_INFO

    if expiration is not None:
        expiration_date = _get_expiration_date_(args)

    else:
        expiration_date = time.time() + DEFAULT_EXPIRATION_TIME

    if  pw is not None:
        if user is None:
            return Ret.RET_ERROR_MISSING_UNSERINFO

        ret_status = server.try_login(user, pw, None)

        if ret_status != Ret.RET_OK:
            return ret_status

        ret_status = crypto.encrypt_information(user,
                                                pw,
                                                expiration_date,
                                                crypto.DataType.DATATYPE_USER_INFO)

    if token is not None:
        ret_status = server.try_login(user, None, token)

        if ret_status != Ret.RET_OK:
            return ret_status

        ret_status = crypto.encrypt_information(user,
                                                token,
                                                expiration_date,
                                                crypto.DataType.DATATYPE_TOKEN_INFO)

    if url is not None:
        if args.default:
            data_type = crypto.DataType.DATATYPE_SERVER_DEFAULT
        else:
            data_type = crypto.DataType.DATATYPE_SERVER

        ret_status = crypto.encrypt_information(url,
                                                None,
                                                expiration_date,
                                                data_type)
    return ret_status

def _delete_login_file(delete_userinfo, delete_token, delete_server, delete_default_server):
    """ _summary_

    Args:
        delete_userinfo (bool):         flag to delete userinfo only
        delete_token (bool):            flag to delete token data
        delete_server (bool):           flag to delete server data
        delete_default_server (bool):   flag to delete default server

    Returns:
        ret_status (Ret): the return status of the module
    """
    if delete_userinfo:
        data_type = crypto.DataType.DATATYPE_USER_INFO
        crypto.delete(data_type)

    if delete_token:
        data_type = crypto.DataType.DATATYPE_TOKEN_INFO
        crypto.delete(data_type)

    if delete_server:
        data_type = crypto.DataType.DATATYPE_SERVER
        crypto.delete(data_type)

    if delete_default_server:
        data_type = crypto.DataType.DATATYPE_SERVER_DEFAULT
        crypto.delete(data_type)

    elif not delete_userinfo and not delete_token and \
       not delete_server and not delete_default_server:
        crypto.delete_all()

    return Ret.RET_OK

def _get_expiration_date_(args):

    input_int = args.expires

    if args.min:
        exp_time = input_int * 60

    elif args.days:
        exp_time = input_int * 24 * 60 * 60

    else:
        exp_time = input_int * 30 * 24 * 60 * 60

    return time.time() + exp_time
