""" Command to delete login information.
    Deletes the stored data files 
    with Userinformation. Either one, some or all
    DataTypes can be deleted with one command.
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
from pyJiraCli.crypto_file_handler import Crypto, DataType
from pyJiraCli.printer import Printer
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
def register(subparser) -> object:
    """ Register subparser commands for the delete module.
        
    Args:
        subparser (obj):   The command subparser object provided via __main__.py.
        
    Returns:
        obj:    The commmand parser object of this module.
    """

    sb_login = subparser.add_parser('delete',
                                    help="delete login information")

    # pylint: disable=duplicate-code

    option_grp = sb_login.add_argument_group('data type to delete')

    option_grp.add_argument('--default',
                            '-d',
                            action='store_true',
                            help="Delete the server URL of the default server.")

    option_grp.add_argument('--userinfo',
                            '-i',
                            action='store_true',
                            help="Delete the user information (username and password).")

    option_grp.add_argument('--server',
                            '-s',
                            action='store_true',
                            help="Delete the server URL of the secondary server.")

    option_grp.add_argument('--token',
                            '-t',
                            action='store_true',
                            help="Delete the API token for Jira server.")

    option_grp.add_argument('--cert',
                            '-c',
                            action='store_true',
                            help="Delete the authentification certificate for Jira server.")

    # pylint: disable=duplicate-code

    return sb_login

def execute(args) -> Ret:
    """ This function servers as entry point for the command 'delete'.
        It will be stored as callback for this moduls subparser command.
    
    Args: 
        args (obj): The command line arguments.
        
    Returns:
        Ret:   Returns Ret.RET_OK if successful or else the corresponding error code.
    """
    return _cmd_delete(args)

def _cmd_delete(args) -> Ret:
    """ Delete login information.
        
    Args:
        args (obj): The command line arguments.
        
    Returns:
        Ret:   Returns Ret.RET_OK if successful or else the corresponding error code.
    """
    ret_status =  _delete_login_file(args.userinfo,
                                     args.token,
                                     args.server,
                                     args.default,
                                     args.cert)
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
        Ret:   Returns Ret.RET_OK if successful or else the corresponding error code.
    """

    printer = Printer()
    crypto_h = Crypto()

    printer.print_info("Deleted stored Information for:")

    if delete_userinfo:
        crypto_h.delete(DataType.DATATYPE_USER_INFO)
        printer.print_info(f"{str(DataType.DATATYPE_USER_INFO)}")

    if delete_token:
        crypto_h.delete(DataType.DATATYPE_TOKEN_INFO)
        printer.print_info(f"{str(DataType.DATATYPE_TOKEN_INFO)}")

    if delete_server:
        crypto_h.delete(DataType.DATATYPE_SERVER)
        printer.print_info(f"{str(DataType.DATATYPE_SERVER)}")

    if delete_default_server:
        crypto_h.delete(DataType.DATATYPE_SERVER_DEFAULT)
        printer.print_info(f"{str(DataType.DATATYPE_SERVER_DEFAULT)}")

    if delete_certificate:
        crypto_h.delete_cert_path()
        crypto_h.delete(DataType.DATATYPE_CERT_INFO)
        printer.print_info(f"{str(DataType.DATATYPE_CERT_INFO)}")

    elif not delete_userinfo and not delete_token and \
         not delete_server and not delete_default_server and \
         not delete_certificate:
        crypto_h.delete_all()
        printer.print_info("All Datatypes and remove the .logindata folder.")

    return Ret.RET_OK
