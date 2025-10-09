""" Command to search for Jira tickets on the provided server.
    Searches for tickets by filter or search str provided via the command line
    and prints all found tickets to command line. """

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
import datetime

from pyJiraCli.file_helper import FileHelper
from pyJiraCli.jira_server import Server
from pyJiraCli.printer import Printer
from pyJiraCli.ret import Ret


################################################################################
# Variables
################################################################################

DEFAULT_FIELDS = ['project', 'summary', 'created', 'creator']
COLUMN_WIDTH = 25
MAX_FIELDS_PRINTED = len(DEFAULT_FIELDS)

LOG = Printer()


################################################################################
# Classes
################################################################################


################################################################################
# Functions
################################################################################

def register(subparser) -> argparse.ArgumentParser:
    """ Register subparser commands for the login module.

    Args:
        subparser (obj):   the command subparser provided via __main__.py

    Returns:
        obj:    the command parser of this module
    """
    # subparser for the 'search' command
    parser = subparser.add_parser(
        'search',
        help="Search for the Jira server for issues using the specified filter string."
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
        'filter',
        type=str,
        help="Filter string to search for. Must be in JQL format."
    )

    parser.add_argument(
        '--max',
        type=int,
        metavar='<MAX>',
        help="Maximum number of issues that may be found." +
        "Default is 50." +
        "If set to 0, all issues will be searched."
    )

    parser.add_argument(
        '--file',
        type=str,
        metavar='<PATH TO FILE>',
        help="Absolute filepath or filepath relative " +
        "to the current work directory to a JSON file."
    )

    parser.add_argument(
        '--full',
        action='store_true',
        required=False,
        help="Get the full information of the issues. " +
        "Can be slow in case of many issues."
    )

    parser.add_argument(
        "--field",
        type=str,
        action="append",
        metavar="<field>",
        required=False,
        help="The field to search for in the issues. " +
        "Can be used multiple times to search for multiple fields."
    )

    parser.add_argument(
        "--translate",
        action="store_true",
        required=False,
        help="Translate the field IDs to names in the output."
    )

    return parser


def execute(args) -> Ret.CODE:
    """ This function servers as entry point for the command 'search'.
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
    else:
        # Get the fields to search for in the issues
        fields = DEFAULT_FIELDS

        if args.full is True:
            fields = []  # Get all fields
        elif args.field is not None:
            fields = args.field  # Get the fields provided by the user

        # Search for the issues
        ret_status = _cmd_search(args.filter,
                                 args.max,
                                 args.file,
                                 server,
                                 fields,
                                 args.translate)

    return ret_status


def _cmd_search(filter_str: str,
                results: int,
                save_file: str,
                server: Server,
                fields: list[str],
                translate: bool) -> Ret.CODE:
    # pylint: disable=too-many-arguments,too-many-positional-arguments
    """ Search tickets with a provided filter or search string.

    Args:
        filter_str (str):   String containing the search parameters.
        results (int):      The maximum number of search results.
        save_file (str):    The absolute filepath or a relative filepath to the current
                            work directory to a JSON file, where the search will be stored.
        server (Server):    The server object to interact with the Jira server.
        fields (list[str]): The fields to search for in the work items.
        translate (bool):   Whether to translate field IDs to names in the output.

    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """
    ret_status = Ret.CODE.RET_OK

    if results is None:
        results = 50

    # Search for the issues on the server.
    ret_status = server.search(filter_str, results, fields)

    if ret_status == Ret.CODE.RET_OK:
        # Retrieve the search result.
        found_issues = server.get_search_result()
        LOG.print_info('Search string:', filter_str)
        LOG.print_info('Found Issues:', str(len(found_issues)))

        search_dict = {
            'search': filter_str,
            'max': results,
            'found': len(found_issues),
            'issues': []
        }

        # Get the Jira handle to request extra data if required.
        jira = server.get_handle()

        for issue in found_issues:
            issue_dict = issue.raw

            # Worklogs are requested for the issue.
            if "worklog" in issue_dict["fields"]:

                # Get the worklogs for the issue
                # Iterate over all worklogs and store them in a list
                worklog_list = [
                    log.raw for log in jira.worklogs(issue.key)]

                issue_dict["fields"]["worklog"] = {
                    "total": len(worklog_list),
                    "worklogs": worklog_list
                }

            # Translate field IDs to names
            if True is translate:
                for field_id in list(issue_dict["fields"].keys()):
                    field_name = server.get_field_name(field_id)
                    issue_dict["fields"][field_name] = issue_dict["fields"].pop(field_id)

            search_dict['issues'].append(issue_dict)

        if save_file is not None:
            ret_status = _save_search(save_file, search_dict)
        else:
            _print_table(search_dict, fields)
            ret_status = Ret.CODE.RET_OK

    return ret_status


def _print_table(search_dict: dict, fields: list[str]) -> None:
    """ Print a quick overview for all issues in the dict.

    Args:
        search_dict (dict): dict with all found issues and search metadata.
    """

    # If all fields are requested, only print the default fields.
    if fields == []:
        fields = DEFAULT_FIELDS

    # Print a maximum of MAX_FIELDS_PRINTED fields.
    issues = search_dict['issues']
    number_of_fields = min(len(fields), MAX_FIELDS_PRINTED)

    # Print the header
    print(f"{'Key':<{COLUMN_WIDTH}}", end="")

    for field_idx in range(number_of_fields):
        print(f"{fields[field_idx]:<{COLUMN_WIDTH}}", end="")
    print()

    # Print the issues
    for issue in issues:
        issue_key = issue['key']
        print(f"{issue_key:<{COLUMN_WIDTH}}", end="")

        for key_idx in range(number_of_fields):
            field_idx = fields[key_idx]
            field_value = issue["fields"][field_idx]

            # If the field value is not a string, try to find its name or print its type.
            if not isinstance(field_value, str):
                if isinstance(field_value, dict) and "name" in field_value:
                    field_value = field_value["name"]
                else:
                    field_value = "Complex Type:" + type(field_value).__name__
            else:
                try:  # Try to convert the field value to a datetime object
                    res = datetime.datetime.strptime(
                        field_value, "%Y-%m-%dT%H:%M:%S.%f%z")
                    field_value = res.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    # Do nothing. The field value is not a datetime object.
                    pass

            # Value is too long for the column and one space.
            if len(field_value) > COLUMN_WIDTH-1:
                # Cut the string by 3 characters and one space, and add "...".
                field_value = field_value[:COLUMN_WIDTH-4] + "..."

            # Print the field value
            print(f"{field_value:<{COLUMN_WIDTH}}", end="")
        print()


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
