""" Command to get the scheme information from the provided server. """

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
    """ Register subparser commands for the scheme module.

    Args:
        subparser (obj):  The command subparser object provided via __main__.py.

    Returns:
        obj:  The command parser object of this module.
    """
    # subparser for the 'scheme' command
    parser = subparser.add_parser(
        'scheme',
        help="Get the scheme information from the Jira server."
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
        '--project',
        type=str,
        metavar='<project>',
        help="The name of the project to get the scheme information for."
    )

    return parser


def execute(args) -> Ret.CODE:
    """ This function servers as entry point for the command 'scheme'.
        It will be stored as callback for this modules subparser command.

    Args:
        args (obj): The command line arguments.

    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
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
    elif args.project:
        ret_status = _get_project_scheme(server, args.project)
    else:
        ret_status = _get_instance_scheme(server)

    return ret_status


def _get_project_scheme(server: Server, project_key: str) -> Ret.CODE:
    """ Get the scheme information from the Jira server for a specific project.

    Args:
        server (Server):    The server object to interact with the Jira server.
        project_key (str):  The key of the project to get the scheme information for.

    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """
    # Initialize output structure
    scheme_output = {
        "project": project_key,
        "issue_types": []
    }

    # Get Jira handle
    jira = server.get_handle()

    # Get project
    try:
        project = jira.project(project_key)
    except Exception:  # pylint: disable=broad-except
        print(f"Project with key '{project_key}' not found.")
        return Ret.CODE.RET_ERROR

    # Get issue types for the project
    issue_types = project.issueTypes
    for issue_type in issue_types:
        element = {
            "name": issue_type.name,
            "id": issue_type.id,
            "description": issue_type.description,
            "is_subtask": issue_type.subtask,
            "fields": []
        }

        # Get fields
        fields = jira.project_issue_fields(project_key, issue_type.id)
        for field in fields:
            field_element = {
                "name": field.raw.get('name', None),
                "id": field.raw.get('fieldId', None),
                "type": field.raw.get('schema', {}).get('type', None),
                "is_required": field.raw.get('required', False),
            }

            element["fields"].append(field_element)

        scheme_output["issue_types"].append(element)

    # Save output to file
    return _save_search(f"scheme_output_{project_key}.json", scheme_output)


def _get_instance_scheme(server: Server) -> Ret.CODE:
    """ Get the scheme information from the Jira server.

    Args:
        server (Server):    The server object to interact with the Jira server.

    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """
    # Initialize output structure
    scheme_output = {
        "issue_types": [],
        "fields": []
    }

    # Get Jira handle
    jira = server.get_handle()

    # Get issue types
    issue_types = jira.issue_types()
    for issue_type in issue_types:
        element = {
            "name": issue_type.name,
            "id": issue_type.id,
            "description": issue_type.description,
            "is_subtask": issue_type.subtask
        }
        scheme_output["issue_types"].append(element)

    # Get fields
    fields = jira.fields()
    for field in fields:
        element = {
            "name": field['name'],
            "id": field['id'],
            "is_custom": field.get('custom', False),
            "type": field.get('schema', {}).get('type', None)
        }
        scheme_output["fields"].append(element)

    # Save output to file
    return _save_search("scheme_output.json", scheme_output)


def _save_search(save_file: str, search_dict: dict) -> Ret.CODE:
    """ Save the search result to a JSON file.

    Args:
        save_file (str): The filepath to the JSON file.
        search_dict (dict): The dictionary with the search data.

    Returns:
        Ret.CODE: _description_
    """
    ret_status = Ret.CODE.RET_OK

    try:
        with FileHelper.open_file(save_file, 'w') as result_file:
            result_data = json.dumps(search_dict, indent=4, ensure_ascii=False)

            result_file.write(result_data)

            msg = f"Successfully saved the search results in '{save_file}'."
            LOG.print_info(msg)
            print(msg)

    except IOError:
        return Ret.CODE.RET_ERROR_FILEPATH_INVALID

    return ret_status
