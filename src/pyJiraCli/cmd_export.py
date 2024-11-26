""" Command to export tickets from jira.
    Issues will be loaded from the server
    and written to a JSON file.
    The file location or file can be provided.
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
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL-
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

################################################################################
# Imports
################################################################################
import json
import argparse

from pyJiraCli.jira_server import Server
from pyJiraCli.file_handler import FileHandler as File
from pyJiraCli.printer import Printer
from pyJiraCli.ret import Ret

################################################################################
# Variables
################################################################################
LOG = Printer()
################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################


def register(subparser) -> argparse.ArgumentParser:
    """ Register the subparser commands for the export module.

    Args:
        subparser (obj):   The command subparser object provided via __main__.py.

    Returns:
        obj:    The command parser obj of this module.
    """

    parser = subparser.add_parser(
        'export',
        help="Export a ticket from a Jira Server to a JSON file."
    )

    parser.add_argument(
        'issue',
        type=str,
        help="Jira issue key"
    )

    parser.add_argument(
        '--profile',
        type=str,
        metavar='<profile>',
        help="The name of the server profile which shall be used for this process."
    )

    parser.add_argument(
        '-u',
        '--user',
        type=str,
        metavar='<user>',
        help="The user to authenticate with the Jira server."
    )

    parser.add_argument(
        '-p',
        '--password',
        type=str,
        metavar='<password>',
        help="The password to authenticate with the Jira server."
    )

    parser.add_argument(
        '-t',
        '--token',
        type=str,
        metavar='<token>',
        help="The token to authenticate with the Jira server."
    )

    parser.add_argument(
        '-s',
        '--server',
        type=str,
        metavar='<server URL>',
        help="The Jira server URL to connect to."
    )

    parser.add_argument(
        '--file',
        type=str,
        metavar='<path to file>',
        help="Absolute file path or filepath relative " +
        "to the current working directory. " +
        "The file format must be JSON. "
        "If a different file format is provided, " +
        "the file extension will be replaced."
    )

    return parser


def execute(args) -> Ret.CODE:
    """ This function servers as entry point for the command 'export'.
        It will be stored as callback for this modules subparser command.

    Args: 
        args (obj): The command line arguments.

    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """
    server = Server()
    ret_status = server.login(  args.profile,
                                args.server,
                                args.token,
                                args.user,
                                args.password)

    if Ret.CODE.RET_OK != ret_status:
        LOG.print_error(
            "Connection to server is not established. Please login first.")
    else:
        ret_status = _cmd_export(args, server)

    return ret_status


def _cmd_export(args, server: Server) -> Ret.CODE:
    """ Export a jira ticket to a JSON file.

        The function takes the command line arguments and extracts the
        provided filepath from -path and -file option.

        If the option -file (filename) is not provided, the function will 
        take the issue key as filename.

        The data will be written and stored in a JSON file.

    Args:
        args (obj): The command line arguments.
        server (Server): The server object to interact with the Jira server.

    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """

    ret_status = Ret.CODE.RET_OK
    file = File()

    ret_status = file.process_file_argument(args.issue,
                                            args.file)
    if ret_status == Ret.CODE.RET_OK:
        ret_status = _export_ticket_to_file(args.issue,
                                            file,
                                            server)

    if ret_status == Ret.CODE.RET_OK:
        LOG.print_info('File saved at:', file.get_path())

    return ret_status


def _export_ticket_to_file(issue_key: str, file: File, server: Server) -> Ret.CODE:
    """ Export a jira issue from the server
        and write the issue data to a JSON file.

    Args:
        issue_key (str):    The issue key as a string.
        file (File):        The file object for the output file.
        server (Server):    The server object to interact with the Jira server.

    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """
    ret_status = server.search(f"key = {issue_key}", max_results=1, fields=[])

    if ret_status == Ret.CODE.RET_OK:

        issue = server.get_search_result().pop().raw

        write_data = json.dumps(issue, indent=4)
        ret_status = file.write_file(write_data)

    return ret_status
