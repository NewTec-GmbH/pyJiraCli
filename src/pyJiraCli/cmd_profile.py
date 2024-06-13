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
import argparse

from pyJiraCli.profile_handler import ProfileHandler
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


def register(subparser) -> argparse.ArgumentParser:
    """ Register subparser commands for the print module.

    Args:
        subparser (obj):   The command subparser object provided via __main__.py.

    Returns:
        obj:    The command parser object of this module.
    """

    sub_parser_profile: argparse.ArgumentParser = \
        subparser.add_parser('profile',
                             help="Add, update or delete server profiles.")

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
                            help="Add a new server profile.")

    option_grp.add_argument('--remove',
                            '-r',
                            action="store_true",
                            help="Delete an existing server profile.")

    option_grp.add_argument('--update',
                            '-u',
                            action="store_true",
                            help="Update an existing server profile with new data.")

    return sub_parser_profile


def execute(args, *_) -> Ret.CODE:
    """ This function servers as entry point for the command 'profile'.
        It will be stored as callback for this modules subparser command.

    Args: 
        args (obj): The command line arguments.
        *_ : Ignore other arguments

    Returns:
        Ret.CODE:   Returns Ret.RET_OK if successful or else the corresponding error code.
    """
    return _cmd_profile(args)


def _cmd_profile(args) -> Ret.CODE:
    """ Process the 'profile' command and its 
        commandline arguments.

    Args:
        args (obj): The commandline arguments.

    Returns:
        Ret.CODE: The return status of the module.
    """

    ret_status = Ret.CODE.RET_OK

    if args.add:
        ret_status = _add_profile(args)

    elif args.remove:
        ret_status = _remove_profile(args.profile_name)

    else:
        ret_status = _update_profile(args)

    return ret_status


def _add_profile(args) -> Ret.CODE:
    """ Adds a new profile to the configuration using provided arguments.

    Args:
        args (obj): Object containing the commandline arguments for profile addition.

    Returns:
        Ret.CODE: Status code indicating the success or failure of the profile addition.
    """
    ret_status = Ret.CODE.RET_OK
    _profile = ProfileHandler()

    if args.url is None:
        ret_status = Ret.CODE.RET_ERROR_NO_SERVER_URL

    else:
        name = args.profile_name
        url = args.url
        token = args.token
        certificate = args.cert
        ret_status = _profile.add(name, url, token, certificate)

    return ret_status


def _remove_profile(profile_name: str) -> Ret.CODE:
    """ Removes a profile from the profile folder by name.

    Args:
        profile_name (str): Name of the profile to be removed.

    Returns:
        Ret.CODE: Status code indicating the success or failure of the profile removal.
    """
    ret_status = Ret.CODE.RET_OK

    ProfileHandler().delete(profile_name)

    return ret_status


def _update_profile(args) -> Ret.CODE:
    """Updates an existing profile in the configuration using provided arguments.

    Args:
        args (obj):  Object containing the commandline arguments for the profile update.

    Returns:
        Ret.CODE: Status code indicating the success or failure of the profile update.
    """
    _profile = ProfileHandler()
    ret_status = _profile.load(args.profile_name)

    if ret_status == Ret.CODE.RET_OK:
        # profile exists

        if args.cert is not None:
            ret_status = _profile.add_certificate(args.profile_name, args.cert)

        if ret_status == Ret.CODE.RET_OK:
            ret_status = _profile.add_token(args.profile_name, args.token)

    return ret_status
