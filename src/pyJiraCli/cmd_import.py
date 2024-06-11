""" Command for the import function.
    Imports ticket information from a JSON file
    and writes the imported data to a Jira ticket.
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
import json

import argparse
from jira.client import JIRA

from pyJiraCli.jira_server import Server
from pyJiraCli.file_handler import FileHandler as File
from pyJiraCli.printer import Printer, PrintType
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
    """ Register subparser commands for the import module.

    Args:
        subparser (obj):  The command subparser object provided via __main__.py.

    Returns:
        obj:  The command parser object of this module.
    """
    sub_parser_import: argparse.ArgumentParser = subparser.add_parser('import',
                                        help="Import a Jira Issue from a JSON file.")

    sub_parser_import.add_argument('file',
                                   type=str,
                                   help="Path to the input file.")

    return sub_parser_import


def execute(args) -> Ret.CODE:
    """ This function servers as entry point for the command 'import'.
        It will be stored as callback for this modules subparser command.

    Args: 
        args (obj):   The command line arguments.
        profile_name (str): The server profile that shall be used.

    Returns:
        Ret:   Ret.CODE.RET_OK if successful, corresponding error code if not
    """

    return _cmd_import(args.file, args.profile)


def _separate_issue_types(issue_dict: dict) -> tuple[list, list]:
    """ Separate the sub-issues from the normal issues.

    Args:
        issue_dict (dict):  The dictionary containing all the issues.

    Returns:
        tuple:  A tuple of Lists containing the main issues and the sub-issues.
    """
    issues_list = []
    sub_issues_list = []

    for issue in issue_dict.get('issues', []):

        # Contains a parent key.
        if "parent" in issue:
            # Is a sub-issue.
            sub_issues_list.append(issue)
        else:
            # Is a normal issue.
            issues_list.append(issue)

    return issues_list, sub_issues_list


def _create_issues(jira: JIRA,
                   printer: Printer,
                   issue_dict: dict,
                   issues_list: list[dict]) -> tuple[Ret.CODE, dict]:
    """ Create the issues on the Jira server.

    Args:
        jira (obj): The Jira handle.
        printer (obj): The printer object.
        issue_dict (dict): The dictionary containing all the issues.
        issues_list (list): The list of normal issues.

    Returns:
        tuple: A tuple of the return status and the ID cross-reference dictionary.
    """
    ret_status = Ret.CODE.RET_OK
    id_cross_ref_dict = {}

    # Create the issues.
    for issue in issues_list:
        # Remove the external ID from the issue dictionary, but store it for later reference.
        external_id = issue.pop('externalId', None)

        if external_id is None:
            ret_status = Ret.CODE.RET_ERROR
            printer.print_error(
                PrintType.ERROR, "External ID must be specified.")
            break

        if external_id in id_cross_ref_dict:
            ret_status = Ret.CODE.RET_ERROR
            printer.print_error(
                PrintType.ERROR, f"External ID {external_id} is not unique.")
            break

        # Set the project key.
        issue['project'] = issue_dict.get('projectKey')

        # Create the issue.
        created_issue = jira.create_issue(issue)

        if created_issue is None:
            ret_status = Ret.CODE.RET_ERROR_CREATING_TICKET_FAILED
            printer.print_error(
                PrintType.ERROR, f"Issue {external_id} could not be created.")
            break

        # Store the external ID and the created issue key in a dictionary for later reference.
        id_cross_ref_dict[external_id] = created_issue.key

        printer.print_info(f"Created issue {created_issue.key}.")

    return ret_status, id_cross_ref_dict


def _create_sub_issues(jira: JIRA,
                       printer: Printer,
                       issue_dict: dict,
                       sub_issues_list: list[dict],
                       id_cross_ref_dict: dict) -> Ret.CODE:
    """ Create the sub-issues on the Jira server.

    Args:
        jira (obj): The Jira handle.
        printer (obj): The printer object.
        issue_dict (dict): The dictionary containing all the issues.
        sub_issues_list (list): The list of sub-issues.
        id_cross_ref_dict (dict): The dictionary containing the cross-reference 
        between external IDs and issue keys.

    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """

    ret_status = Ret.CODE.RET_OK

    # Create the sub-issues.
    for issue in sub_issues_list:
        # Remove external id from the issue dictionary.
        external_id = issue.pop('externalId', None)

        # Set the project key.
        issue['project'] = issue_dict.get('projectKey')

        # Check if the parent issue key is specified,
        # in case the sub-issue belongs to an issue that was manually created before.
        if issue.get('parent').get('key') is None:

            # Check if the parent external ID is specified,
            # in case the sub-issue belongs to an issue that was created in this import process.
            parent_external_id = issue.get('parent').get('externalId')

            if parent_external_id is None:
                # Both parent key and external ID are missing.
                ret_status = Ret.CODE.RET_ERROR
                printer.print_error(
                    PrintType.ERROR, "Parent key or external ID must be specified.")
                break

            if parent_external_id not in id_cross_ref_dict:
                # Parent external ID does not exist.
                ret_status = Ret.CODE.RET_ERROR
                printer.print_error(
                    PrintType.ERROR, f"Parent external ID\
                            {parent_external_id} does not exist.")
                break

            # Set the parent key from the cross reference dictionary,
            # as the issue was created by _create_issues() function.
            issue['parent']["key"] = id_cross_ref_dict[parent_external_id]

        # Remove the external ID from the parent issue dictionary in case its present.
        issue['parent'].pop('externalId', None)

        # Create the sub-issue.
        created_issue = jira.create_issue(issue)

        if created_issue is None:
            ret_status = Ret.CODE.RET_ERROR_CREATING_TICKET_FAILED
            printer.print_error(
                PrintType.ERROR, f"Sub-issue {external_id} could not be created.")
            break

        printer.print_info(
            f"Created sub-issue {created_issue.key} with parent {issue.get('parent').get('key')}.")

    return ret_status


def _cmd_import(input_file: str, profile_name: str) -> Ret.CODE:
    """ Import a jira issue from a JSON file.
        Create a jira issue on the server with the data
        read from the input file.

    Args:
        input_file (str):  The filepath to the input file.
        profile_name (str): The server profile that shall be used.


    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """
    server = Server()
    printer = Printer()
    issue_dict = {}

    # Read the data from the file.
    ret_status, issue_dict = _read_file(input_file)

    if Ret.CODE.RET_OK == ret_status:
        # Connect to Jira Server
        ret_status = server.login(profile_name)

    if Ret.CODE.RET_OK == ret_status:
        # Get the Jira handle to use the Jira API directly.
        jira = server.get_handle()

        # Check if the project key is specified.
        project_key = issue_dict.get('projectKey', {}).get('key')

        if project_key is None:
            ret_status = Ret.CODE.RET_ERROR
            printer.print_error(
                PrintType.ERROR, "Project key must be specified.")

    if Ret.CODE.RET_OK == ret_status:
        issues_list = []
        sub_issues_list = []
        id_cross_ref_dict = {}

        # Separate the sub-issues from the normal issues.
        issues_list, sub_issues_list = _separate_issue_types(issue_dict)

        # Create the normal issues.
        ret_status, id_cross_ref_dict = _create_issues(jira,
                                                       printer,
                                                       issue_dict,
                                                       issues_list)

        # Check if the issues were created successfully.
        if Ret.CODE.RET_OK == ret_status:
            # Create the sub issues.
            ret_status = _create_sub_issues(jira,
                                            printer,
                                            issue_dict,
                                            sub_issues_list,
                                            id_cross_ref_dict)

    return ret_status


def _read_file(input_file: str) -> tuple[Ret.CODE, dict]:
    """ Read in the data from a JSON file.

    Args:
        file (str): The filepath to the input file.

    Returns:
        tuple:  A tuple of the return status and the issue dictionary from the file.
    """
    issue_dict = {}
    file = File()

    # Locate file.
    ret_status = file.set_filepath(input_file)

    if Ret.CODE.RET_OK == ret_status:
        # Check if file is a JSON file and open it.
        if file.get_file_extension() != '.json':
            ret_status = Ret.CODE.RET_ERROR_WORNG_FILE_FORMAT
        elif Ret.CODE.RET_OK != file.open_file(file_mode='r'):
            ret_status = Ret.CODE.RET_ERROR_FILE_OPEN_FAILED
        else:
            issue_dict = json.load(file.get_file())
            file.close_file()
            ret_status = Ret.CODE.RET_OK

    return ret_status, issue_dict
