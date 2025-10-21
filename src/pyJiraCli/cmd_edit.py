""" Command for the edit function.
    Read ticket information from a JSON file
    and edits the imported data to an existing Jira ticket.
"""

# BSD 3-Clause License
#
# Copyright (c) 2024 - 2025, NewTec GmbH
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

import json
import os

import argparse

from pyJiraCli.file_helper import FileHelper
from pyJiraCli.jira_server import Server
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
    """ Register subparser commands for the edit module.

    Args:
        subparser (obj):  The command subparser object provided via __main__.py.

    Returns:
        obj:  The command parser object of this module.
    """
    parser = subparser.add_parser(
        'edit',
        help="Edit Jira Issues from a JSON file."
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
        'file',
        type=str,
        help="Path to the input file."
    )

    return parser


def execute(args) -> Ret.CODE:
    """ This function servers as entry point for the command 'import'.
        It will be stored as callback for this modules subparser command.

    Args:
        args (obj):   The command line arguments.

    Returns:
        Ret:   Ret.CODE.RET_OK if successful, corresponding error code if not
    """
    server = Server()
    ret_status = server.login(args.profile,
                              args.server,
                              args.token,
                              args.user,
                              args.password)

    if Ret.CODE.RET_OK != ret_status:
        LOG.print_error(
            "Connection to server is not established. Please login first.")
    else:
        ret_status = _cmd_import(args.file, server)

    return ret_status


def _cmd_import(input_file: str, server: Server) -> Ret.CODE:
    """ Import a jira issue from a JSON file.
        Create a jira issue on the server with the data
        read from the input file.

    Args:
        input_file (str):  The filepath to the input file.
        server (Server): The server object to interact with the Jira server.

    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """

    issue_dict = {}

    # Read the data from the file.
    ret_status, issue_dict = _read_json_file(input_file)

    if Ret.CODE.RET_OK == ret_status:
        # Get the Jira handle to use the Jira API directly.
        jira = server.get_handle()

        # Get the issues to edit.
        issues_to_edit = issue_dict.get('issues', [])

        for input_issue in issues_to_edit:
            # Get only the fields to update.
            fields_to_update = input_issue.get('fields', {}).keys()
            LOG.print_info(f"Editing {input_issue['key']}: {fields_to_update}")

            # Retrieve the issue object.
            issue_object = jira.issue(input_issue['key'], fields=fields_to_update)

            # Update the issue with the new data.
            issue_object.update(fields=input_issue['fields'])

    return ret_status


def _read_json_file(input_file: str) -> tuple[Ret.CODE, dict]:
    """ Read in the data from a JSON file.

    Args:
        file (str): The filepath to the input file.

    Returns:
        tuple:  A tuple of the return status and the issue dictionary from the file.
    """

    issue_dict = {}
    ret_status = Ret.CODE.RET_OK

    # Make sure file has .json extension.
    if os.path.splitext(input_file)[-1] != '.json':
        return Ret.CODE.RET_ERROR_WRONG_FILE_FORMAT

    try:
        with FileHelper.open_file(input_file, 'r') as input_file_handle:
            issue_dict = json.load(input_file_handle)

    except IOError:
        ret_status = Ret.CODE.RET_ERROR_FILEPATH_INVALID

    return ret_status, issue_dict
