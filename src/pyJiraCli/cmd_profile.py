""" Command for the profile function.
    This module caan add, remove or configure server profiles.
    The profiles contain server url, login data, the server certificate
    and configuration data for a specific jira server instance.
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
from pyJiraCli.jira_server import Server
from pyJiraCli.profile import Profile
from pyJiraCli.ret import Ret
################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################
def register(subparser) -> object:
    """ Register subparser commands for the print module.
        
    Args:
        subparser (obj):   The command subparser object provided via __main__.py.
        
    Returns:
        obj:    The commmand parser object of this module.
    """

    sub_parser_profile = subparser.add_parser('profile',
                                      help="Print the Jira Issue details to the console.")

    login_group = sub_parser_profile.add_argument_group("Profile Data")

    login_group.add_argument('profile_name',
                            type=str,
                            metavar="<profile name>",
                            help="The Name under which the profile will be saved.")

    login_group.add_argument('--url',
                            type=str,
                            metavar="<profile url>",
                            help="The server url for the profile.")


    login_group.add_argument("--token",
                             type=str,
                             metavar="<api token>",
                             help="The api token for login with this server profile")

    login_group.add_argument('--cert',
                            type=str,
                            metavar="<certificate path>",
                            required=False,
                            help="The server url for the profile.")

    datatype_desc = sub_parser_profile.add_argument_group(
        title='profile operations',
        description='Only one operation type can be processed at a time.'
    )

    option_grp = datatype_desc.add_mutually_exclusive_group(required=True)

    option_grp.add_argument('--add',
                           '-a',
                            action="store_true",
                            help="The server url for the profile.")

    option_grp.add_argument('--remove',
                           '-r',
                            action="store_true",
                            help="The server url for the profile.")

    option_grp.add_argument('--confiq',
                           '-c',
                            action="store_true",
                            help="The server url for the profile.")


    return sub_parser_profile

def execute(args) -> Ret:
    """ This function servers as entry point for the command 'print'.
        It will be stored as callback for this moduls subparser command.
    
    Args: 
        args (obj): The command line arguments.
        
    Returns:
        Ret:   Returns Ret.RET_OK if successful or else the corresponding error code.
    """
    return _cmd_profile(args)

def _cmd_profile(args) -> Ret:
    """Load the data of the provided issue key and 
        and print it to the command line.

    Args:
        issue_key (str): the unique issue key in string format
        user (str): username for login
        pw (str): password for login

    Returns:
        retval.Ret: return status of the module
    """

    ret_status = Ret.CODE.RET_OK

    if args.add:
        ret_status = _add_profile(args)

    elif args.remove:
        ret_status = _remove_profile(args.profile_name)

    else:
        ret_status = _configure_profile(args)

    return ret_status



def _add_profile(args):
    ret_status = Ret.CODE.RET_OK

    _server = Server()
    _profile = Profile()

    if args.url is None:
        ret_status = Ret.CODE.RET_ERROR_NO_SERVER_URL

    else:
        name = args.profile_name
        url = args.url
        token = args.token
        certificate = args.cert

        ret_status = _server.try_login(url, token, certificate)

        if ret_status == Ret.CODE.RET_OK:
            ret_status = _profile.add(name, url, token, certificate)

    return ret_status

def _remove_profile(profile_name:str):
    ret_status = Ret.CODE.RET_OK
    print(f"remove Profile {profile_name}")
    return ret_status

def _configure_profile(args):
    ret_status = Ret.CODE.RET_OK
    print(f"configure Profile {args.profile_name}")
    return ret_status
