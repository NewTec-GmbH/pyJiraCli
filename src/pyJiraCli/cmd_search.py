""" Command to search for Jira tickets on the provided server.
    Searches for tickets by filter or search str provided via the command line 
    and prints all found tickets to command line. """

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
import json
import argparse
import datetime

from pyJiraCli.jira_server import Server
from pyJiraCli.file_handler import FileHandler as File
from pyJiraCli.printer import Printer
from pyJiraCli.ret import Ret
################################################################################
# Variables
################################################################################

DEFAULT_FIELDS = ['project', 'summary', 'created', 'creator']
COLUMN_WIDTH = 25

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
    sub_parser_search: argparse.ArgumentParser = \
        subparser.add_parser('search',
                             help="Search for the Jira server for issues " +
                             "using the specified filter string.")

    sub_parser_search.add_argument('filter',
                                   type=str,
                                   help="Filter string to search for. Must be in JQL format.")

    sub_parser_search.add_argument('--max',
                                   type=int,
                                   metavar='<MAX>',
                                   help="Maximum number of issues that may be found." +
                                   "Default is 50." +
                                   "If set to 0, all issues will be searched.")

    sub_parser_search.add_argument('--file',
                                   type=str,
                                   metavar='<PATH TO FILE>',
                                   help="Absolute filepath or filepath relative " +
                                   "to the current work directory to a JSON file.")

    sub_parser_search.add_argument('--full',
                                   action='store_true',
                                   required=False,
                                   help="Get the full information of the issues. " +
                                   "Can be slow in case of many issues.")

    sub_parser_search.add_argument("--field",
                                   type=str,
                                   action="append",
                                   metavar="<field>",
                                   required=False,
                                   help="The field to search for in the issues. " +
                                   "Can be used multiple times to search for multiple fields.")

    return sub_parser_search


def execute(args, server: Server) -> Ret.CODE:
    """ This function servers as entry point for the command 'search'.
        It will be stored as callback for this modules subparser command.

    Args: 
        args (obj): The command line arguments.
        server (Server): The server object to interact with the Jira server.

    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """
    ret_status = Ret.CODE.RET_ERROR

    # pylint: disable=R0801
    if server is None:
        LOG.print_error(
            "Connection to server is not established. Please login first.")
    else:
        fields = DEFAULT_FIELDS

        if args.full is True:
            fields = []  # Get all fields
        elif args.field is not None:
            fields = args.field  # Get the fields provided by the user

        ret_status = _cmd_search(
            args.filter, args.max, args.file, server, fields)

    return ret_status


def _cmd_search(filter_str: str,
                results: int,
                save_file: str,
                server: Server,
                fields: list[str]) -> Ret.CODE:
    """ Search tickets with a provided filter or search string.

    Args:
        filter_str (str):   String containing the search parameters.
        results (int):      The maximum number of search results.
        save_file (str):    The absolute filepath or a relative filepath to the current
                            work directory to a JSON file, where the search will be stored.
        server (Server):    The server object to interact with the Jira server.
        fields (list[str]): The fields to search for in the work items.

    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """
    ret_status = Ret.CODE.RET_OK

    if results is None:
        results = 50

    ret_status = server.search(filter_str, results, fields)

    if ret_status == Ret.CODE.RET_OK:
        found_issues = server.get_search_result()
        LOG.print_info('Search string:', filter_str)
        LOG.print_info('Found Issues:', str(len(found_issues)))

        search_dict = {
            'search': filter_str,
            'max': results,
            'found': len(found_issues)
        }

        issue_list = []
        jira = server.get_handle()

        for issue in found_issues:
            issue_dict = issue.raw

            # Worklogs are requested for the issue.
            if "worklog" in issue_dict["fields"]:

                # Get the worklogs for the issue
                # Itereate over all worklogs and store them in a list
                worklog_list = [
                    log.raw for log in jira.worklogs(issue.key)]

                issue_dict["fields"]["worklog"] = {
                    "total": len(worklog_list),
                    "worklogs": worklog_list
                }

            issue_list.append(issue_dict)

        search_dict['issues'] = issue_list

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

    if fields == []:
        fields = DEFAULT_FIELDS

    issues = search_dict['issues']
    number_of_fields = min(len(fields), 5)

    print(f"{'Key':<{COLUMN_WIDTH}}", end="")

    for field in range(number_of_fields):
        print(f"{fields[field]:<{COLUMN_WIDTH}}", end="")
    print()

    for issue in issues:
        issue_key = issue['key']
        print(f"{issue_key:<{COLUMN_WIDTH}}", end="")

        for key in range(number_of_fields):
            field = fields[key]
            field_value = issue["fields"][field]

            if not isinstance(field_value, str):
                field_value = "<complex>"
            else:
                try:  # Try to convert the field value to a datetime object
                    res = datetime.datetime.strptime(
                        field_value, "%Y-%m-%dT%H:%M:%S.%f%z")
                    field_value = res.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    pass  # Do nothing

            if len(field_value) > COLUMN_WIDTH-1:
                field_value = field_value[:COLUMN_WIDTH-4] + "..."

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

    file = File()

    write_data = json.dumps(search_dict, indent=4)

    ret_status = file.set_filepath(save_file)

    if ret_status == Ret.CODE.RET_OK:
        ret_status = file.write_file(write_data)

    if ret_status == Ret.CODE.RET_OK:
        LOG.print_info("Search was saved in file:", save_file)

    return ret_status
