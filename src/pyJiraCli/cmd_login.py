""" Command to store login information.
    Stores User, pw and a server url in an encoded file
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
from datetime import datetime

from pyJiraCli.crypto_file_handler import Crypto, DataType
from pyJiraCli.jira_server import Server
from pyJiraCli.ret import Ret
from pyJiraCli.printer import Printer

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
def register(subparser) -> object:
    """ Register subparser commands for the login module.
        
    Args:
        subparser (obj):   The command subparser object provided via __main__.py.
        
    Returns:
        obj:    The commmand parser object of this module.
    """

    sb_login = subparser.add_parser('login',
                                    help="save login information")

    data_grp = sb_login.add_argument_group('data')

    data_grp.add_argument('data1',
                           type=str,
                           metavar='<data1>',
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

    # pylint: disable=duplicate-code

    option_grp = sb_login.add_argument_group('data type to store')

    option_grp.add_argument('--default',
                            '-d',
                            action='store_true',
                            help="primary server url to use")

    option_grp.add_argument('--userinfo',
                            '-ui',
                            action='store_true',
                            help="username, pw")

    option_grp.add_argument('--server',
                            '-s',
                            action='store_true',
                            help="secondary server url to use")

    option_grp.add_argument('--token',
                            '-t',
                            action='store_true',
                            help="API token for jira server")

    option_grp.add_argument('--cert',
                            '-c',
                            action='store_true',
                            help="authentification certificate for jira server")

    # pylint: enable=duplicate-code

    return sb_login

def execute(args) -> Ret:
    """ This function servers as entry point for the command 'login'.
        It will be stored as callback for this moduls subparser command.
    
    Args: 
        args (obj): The command line arguments.
        
    Returns:
        Ret:   Returns Ret.RET_OK if successful or else the corresponding error code.
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

    if args.data1 is None and args.data2 is None :
        ret_status = Ret.RET_ERROR_MISSING_LOGIN_DATA
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
        Ret:   Returns Ret.RET_OK if successful or else the corresponding error code.
    """
    ret_status = Ret.RET_OK

    data1 = None # username, token, url or path
    data2 = None # optional: pw only with username
    expiration = args.expires

    if args.userinfo:
        data1 = args.data1
        data2 = args.data2

    else:
        data1 = args.data1

    if expiration is not None:
        expiration_date = _get_expiration_date_(args)
    else:
        expiration_date = time.time() + DEFAULT_EXPIRATION_TIME

    ret_status = _store_information(data1, data2, args, expiration_date)

    return ret_status

def _store_information(data1:str, data2:str, args:object, expiration_date:float) -> Ret:
    """ Store the information in encrypted files
        with the crypto_filehandler.

    Args:
        data1 (str): Data1 is either Token, Server, Certificate path or Username.
        data2 (str): Data2 is a password if data1 is a username.
        args (object): The command line arguments.
        expiration_date (float): The expiration date for this information.

    Returns:
        Ret:   Returns Ret.RET_OK if successful or else the corresponding error code.
    """

    crypto_h = Crypto()
    server = Server()
    printer = Printer()

    data_type = None

    if args.server or args.default:
        if args.default:
            data_type = DataType.DATATYPE_SERVER_DEFAULT
        else:
            data_type = DataType.DATATYPE_SERVER

        crypto_h.set_data(data1)
        ret_status = crypto_h.encrypt_information(expiration_date, data_type)

    elif args.userinfo:
        data_type = DataType.DATATYPE_USER_INFO
        if data2 is None:
            ret_status = Ret.RET_ERROR_MISSING_UNSERINFO

        else:
            ret_status = server.try_login(data1, data2, None)

        if ret_status == Ret.RET_OK:
            crypto_h.set_data(data1, data2)
            ret_status = crypto_h.encrypt_information(expiration_date, DataType.DATATYPE_USER_INFO)

    elif args.token:
        data_type = DataType.DATATYPE_TOKEN_INFO
        ret_status = server.try_login(None, None, data1)

        if ret_status == Ret.RET_OK:
            crypto_h.set_data(data1)
            ret_status = crypto_h.encrypt_information(expiration_date, DataType.DATATYPE_TOKEN_INFO)

    elif args.cert:
        data_type = DataType.DATATYPE_CERT_INFO
        ret_status = crypto_h.store_certificate(data1, expiration_date)

    else:
        ret_status = Ret.RET_ERROR_MISSING_DATATYPE

    if ret_status == Ret.RET_OK:
        # Convert epoch time to datetime object
        dt = datetime.fromtimestamp(expiration_date)

        # Format datetime object to desired string format
        formatted_time = dt.strftime('%d/%m/%Y %H:%M:%S')

        printer.print_info("Stored the information for DataType:",
                            str(data_type))
        printer.print_info("Expiration date for the data:",
                            formatted_time)

    return ret_status

def _get_expiration_date_(args) -> float:
    """ Calculate the expiration date 
        from the commandline arguments in epoch seconds.

    Args:
        args (obj): The commandline arguments.

    Returns:
        float: The time in Epoch seconds when the files will expire.
    """

    input_int = args.expires

    if args.min:
        exp_time = input_int * 60

    elif args.day:
        exp_time = input_int * 24 * 60 * 60

    else:
        exp_time = input_int * 30 * 24 * 60 * 60

    return time.time() + exp_time
