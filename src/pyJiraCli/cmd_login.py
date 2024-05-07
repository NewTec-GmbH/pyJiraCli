""" Command to store login information.
    Stores User, pw and a server url in an encoded file
    or deltes stored login informations.
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
import time

from pyJiraCli.crypto_file_handler import Crypto, DataType
from pyJiraCli.jira_server import Server
from pyJiraCli.ret import Ret

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
def register(subparser) -> object:
    """ Register subparser commands for the login module.
        
    Args:
        subparser (obj):   The command subparser object provided via __main__.py.
        
    Returns:
        obj:    The commmand parser object of this module.
    """

    sb_login = subparser.add_parser('login',
                                    help="save or delete login information")

    data_grp = sb_login.add_argument_group('data')

    data_grp.add_argument('data1',
                           type=str,
                           metavar='<data1>',
                           nargs='?',
                           help="<username, token, url>")

    data_grp.add_argument('data2',
                           type=str,
                           metavar='<data2>',
                           nargs='?',
                           help="optional <password>")

    sb_login.add_argument('-expires',
                           type=int,
                           metavar='<time>',
                           help="time after which the stored login info \
                                 will expire. default = 30 days")

    expire_grp = sb_login.add_argument_group('expiry options')

    expire_grp.add_argument('--min',
                           action='store_true',
                           help="expire time in minutes")

    expire_grp.add_argument('--day',
                           action='store_true',
                           help="expire time in days")

    expire_grp.add_argument('--month',
                           action='store_true',
                           help="expire time in months")

    sb_login.add_argument('-delete',
                           action='store_true',
                           help="delete login information")

    option_grp = sb_login.add_argument_group('data type to store or delete')

    option_grp.add_argument('--default',
                            '-d',
                            action='store_true',
                            help="default server url")

    option_grp.add_argument('--userinfo',
                            '-ui',
                            action='store_true',
                            help="username, pw")

    option_grp.add_argument('--server',
                            '-s',
                            action='store_true',
                            help="primary server url to use")

    option_grp.add_argument('--token',
                            '-t',
                            action='store_true',
                            help="API token for jira server")

    option_grp.add_argument('--cert',
                            '-c',
                            action='store_true',
                            help="authentification certificate for jira server")

    return sb_login

def execute(args) -> Ret:
    """ This function servers as entry point for the command 'login'.
        It will be stored as callback for this moduls subparser command.
    
    Args: 
        args (obj): The command line arguments.
        
    Returns:
        Ret:   Returns Ret.RET_OK if succesfull or the corresponding error code if not.
    """
    return _cmd_login(args)

def _cmd_login(args) -> Ret:
    """ Store or delete login information.
        
    Args:
        args (obj): The command line arguments.
        
    Returns:
        Ret:   Ret.RET_OK if succesfull, corresponding error code if not
    """
    ret_status = Ret.RET_OK

    if args.delete:
        ret_status =  _delete_login_file(args.userinfo,
                                         args.token,
                                         args.server,
                                         args.default,
                                         args.cert)

    else:
        ret_status = _store_login_info(args)

    return ret_status

def _store_login_info(args) -> Ret:
    """ Save the login info in a encrypted file.
        userinfo(user, pw), token, server and default server
        are all saved in seperate files.
        
    Args:
        args (obj): The commnd line arguments.

    Returns:
        Ret:   Returns Ret.RET_OK if succesfull or the corresponding error code if not.
    """
    ret_status = Ret.RET_OK

    crypto_h = Crypto()
    server = Server()

    data1 = None # username, token, url or path
    data2 = None # optional: pw only with username

    if args.userinfo:
        data1 = args.data1
        data2 = args.data2

    else:
        data1 = args.data1

    if data1 is None and data2 is None :
        ret_status = Ret.RET_ERROR_MISSING_ARG_INFO

    if ret_status == Ret.RET_OK:
        expiration_date = _get_expiration_date_(args)

        if args.server or args.default:
            if args.default:
                data_type = DataType.DATATYPE_SERVER_DEFAULT
            else:
                data_type = DataType.DATATYPE_SERVER

            crypto_h.set_data(data1)
            ret_status = crypto_h.encrypt_information(expiration_date, data_type)

        elif args.userinfo:
            if data2 is None:
                return Ret.RET_ERROR_MISSING_UNSERINFO

            ret_status = server.try_login(data1, data2, None)

            if ret_status != Ret.RET_OK:
                return ret_status

            crypto_h.set_data(data1, data2)
            ret_status = crypto_h.encrypt_information(expiration_date, DataType.DATATYPE_USER_INFO)

        elif args.token:
            ret_status = server.try_login(None, None, data1)

            if ret_status != Ret.RET_OK:
                return ret_status

            crypto_h.set_data(data1)
            ret_status = crypto_h.encrypt_information(expiration_date, DataType.DATATYPE_TOKEN_INFO)

        elif args.cert:
            ret_status = crypto_h.store_certificate(data1, expiration_date)

    return ret_status

def _delete_login_file(delete_userinfo:bool,
                       delete_token:bool,
                       delete_server:bool,
                       delete_default_server:bool,
                       delete_certificate:bool) -> Ret:
    """ Delete the login files corresponding to the set dataType flags.

    Args:
        delete_userinfo (bool):         Flag to delete userinfo data.
        delete_token (bool):            Flag to delete token data.
        delete_server (bool):           Flag to delete server data.
        delete_default_server (bool):   Flag to delete default server.
        delete_certificate (bool):      Flag to delete the server certificate.

    Returns:
        Ret:   Returns Ret.RET_OK if succesfull or the corresponding error code if not.
    """
    crypto_h = Crypto()

    if delete_userinfo:
        crypto_h.delete(DataType.DATATYPE_USER_INFO)

    if delete_token:
        crypto_h.delete(DataType.DATATYPE_TOKEN_INFO)

    if delete_server:
        crypto_h.delete(DataType.DATATYPE_SERVER)

    if delete_default_server:
        crypto_h.delete(DataType.DATATYPE_SERVER_DEFAULT)

    if delete_certificate:
        crypto_h.delete_cert_path()
        crypto_h.delete(DataType.DATATYPE_CERT_INFO)

    elif not delete_userinfo and not delete_token and \
         not delete_server and not delete_default_server and \
         not delete_certificate:
        crypto_h.delete_all()

    return Ret.RET_OK

def _get_expiration_date_(args) -> float:
    """ Calculate the expiration date 
        from the commandline arguments in epoch seconds.

    Args:
        args (obj): The commandline arguments.

    Returns:
        float: The time in Epoch seconds when the files will expire.
    """

    input_int = args.expires

    if input_int is None:
        input_int = DEFAULT_EXPIRATION_TIME

    elif args.min:
        exp_time = input_int * 60

    elif args.days:
        exp_time = input_int * 24 * 60 * 60

    else:
        exp_time = input_int * 30 * 24 * 60 * 60

    return time.time() + exp_time
