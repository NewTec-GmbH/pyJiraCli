""" Command for the import function.
    Imports ticket information from a json or csv file
    and writes the imported data to a jira ticket.
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
import csv
import ast

from pyJiraCli.jira_issue import _const
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
def register(subparser) -> object:
    """ Register subparser commands for the import module.
        
    Args:
        subparser (obj):  The command subparser object provided via __main__.py.
        
    Returns:
        obj:  The commmand parser object of this module.
    """
    sub_parser_import = subparser.add_parser('import',
                                      help="Import a Jira Issue from a JSON or a CSV file.")

    sub_parser_import.add_argument('file',
                            type=str,
                            help="Path to the input file.")

    return sub_parser_import

def execute(args) -> Ret.CODE:
    """ This function servers as entry point for the command 'import'.
        It will be stored as callback for this moduls subparser command.
    
    Args: 
        args (obj):   The command line arguments.
        profile_name (str): The server profile that shall be used.
        
    Returns:
        Ret:   Ret.CODE.RET_OK if succesfull, corresponding error code if not
    """
    ret_status = Ret.CODE.RET_OK

    ret_status =  _cmd_import(args.file, args.profile)

    return ret_status


def _cmd_import(input_file: str, profile_name: str) -> Ret.CODE:
    """ Import a jira issue from a json or csv file.
        Create a jira issue on the server with the data
        read from the input file.
    
    Args:
        input_file (str):  The filepath to the input file.
        
        
    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """
    server = Server()
    printer = Printer()
    file = File()
    issue_dict = {}

    # Locate file.
    ret_status = file.set_filepath(input_file)

    if ret_status == Ret.CODE.RET_OK:
        # Check if file is a json file and open it.
        if file.get_file_extension() != '.json':
            ret_status = Ret.CODE.RET_ERROR_WORNG_FILE_FORMAT
        else:
            ret_status = file.open_file(file_mode='r')

    if ret_status == Ret.CODE.RET_OK:
        # Read in the data from the file.
        issue_dict = _read_file(file)

        # Connect to Jira Server
        ret_status = server.login(profile_name)

    if ret_status == Ret.CODE.RET_OK:
        # Get the Jira handle to use the Jira API directly.
        jira = server.get_handle()

        # Check if the project key is specified.
        project_key = issue_dict.get('projectKey', {}).get('key')

        if project_key is None:
            ret_status = Ret.CODE.RET_ERROR
            printer.print_error(
                PrintType.ERROR, "Project key must be specified.")

    if ret_status == Ret.CODE.RET_OK:
        issues_list = []
        sub_issues_list = []
        id_cross_ref_dict = {}

        # Check if the issues are sub-issues or not.
        for issue in issue_dict.get('issues', []):

            # Contains a parent key.
            if "parent" in issue:
                # Is a sub-issue.
                sub_issues_list.append(issue)
            else:
                # Is a normal issue.
                issues_list.append(issue)

        # Create the issues.
        for issue in issues_list:
            # External ID must be specified to create the issue.
            external_id = issue.get('externalId')

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

            # Remove the external ID from the issue dictionary, but store it for later reference.
            issue.pop('externalId', None)

            # Set the project key.
            issue['project'] = issue_dict.get('projectKey')

            # Create the issue.
            created_issue = jira.create_issue(issue)

            if created_issue is None:
                ret_status = Ret.CODE.RET_ERROR
                # "Issue could not be created."
                break

            # Store the external ID and the created issue key in a dictionary for later reference.
            id_cross_ref_dict[external_id] = created_issue.key

            printer.print_info(f"Created issue {created_issue.key}.")

        # Check if the issues were created successfully.
        if ret_status == Ret.CODE.RET_OK:

            # Create the sub-issues.
            for issue in sub_issues_list:
                # Remove external id from the issue dictionary.
                issue.pop('externalId', None)

                # Set the project key.
                issue['project'] = issue_dict.get('projectKey')

                # Check if the parent key is specified.
                if issue.get('parent').get('key') is None:
                    parent_external_id = issue.get('parent').get('externalId')

                    if parent_external_id is None:
                        ret_status = Ret.CODE.RET_ERROR
                        printer.print_error(
                            PrintType.ERROR, "Parent key or external ID must be specified.")
                        break

                    if parent_external_id not in id_cross_ref_dict:
                        ret_status = Ret.CODE.RET_ERROR
                        printer.print_error(
                            PrintType.ERROR, f"Parent external ID\
                                  {parent_external_id} does not exist.")
                        break

                    # Set the parent key.
                    issue['parent']["key"] = id_cross_ref_dict[parent_external_id]

                # Create the sub-issue.
                created_issue = jira.create_issue(issue)

                # Remove the external ID from the parent issue dictionary in case its present.
                issue['parent'].pop('externalId', None)

                if created_issue is None:
                    ret_status = Ret.CODE.RET_ERROR
                    # "Sub-issue could not be created."
                    break

                printer.print_info(
                    f"Created sub-issue {created_issue.key} with\
                          parent {issue.get('parent').get('key')}.")

    # Logout from the server.
    server.logout()

    return ret_status


def _read_file(file:File) -> dict:
    """ Read in the data from a json or csv file.

    Args:
        file (FileHandler): The file handler obj for the input file.
    
    Returns:
        dict:  The dictionary with file informations.   
    """
    if file.get_file_extension() == '.json':
        issue_dict = json.load(file.get_file())

    else:
        csv_reader = csv.DictReader(file.get_file(), delimiter=';')

        for row in csv_reader:
            issue_dict = row

        for field, data in issue_dict.items():
            if data == '':
                issue_dict[field] = None

            elif data == '[]':
                issue_dict[field] = []

            elif field in _const.LIST_FIELDS:
                issue_dict[field] = ast.literal_eval(data)

    file.close_file()

    return issue_dict
