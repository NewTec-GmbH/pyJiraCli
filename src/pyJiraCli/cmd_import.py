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

from pyJiraCli.jira_issue import JiraIssue, _const
from pyJiraCli.jira_server import Server
from pyJiraCli.file_handler import FileHandler as File
from pyJiraCli.printer import Printer
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

def _cmd_import(input_file:str, profile_name:str) -> Ret.CODE:
    """ Import a jira issue from a json or csv file.
        Create a jira issue on the server with the data
        read from the input file.
    
    Args:
        input_file (str):  The filepath to the input file.
        
        
    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """
    ret_status = Ret.CODE.RET_OK

    issue = JiraIssue()
    server = Server()
    printer = Printer()
    file = File()

    issue_dict = {}
    issue_key = None


    # check if provided file is viable
    ret_status = file.set_filepath(input_file)

    if ret_status == Ret.CODE.RET_OK:
        if file.get_file_extension() not in ('.json', '.csv'):
            ret_status = Ret.CODE.RET_ERROR_WORNG_FILE_FORMAT
    else:
        ret_status = Ret.CODE.RET_ERROR_FILEPATH_INVALID

    # if file is viable
    if ret_status == Ret.CODE.RET_OK:

        ret_status = file.open_file(file_mode='r')

    if ret_status == Ret.CODE.RET_OK:
        issue_dict = _read_file(file)

        issue.import_issue(issue_dict)

    if ret_status == Ret.CODE.RET_OK:
        ret_status = server.login(profile_name)

        if ret_status == Ret.CODE.RET_OK:
            jira = server.get_handle()
            issue_key = issue.create_ticket(jira)

    if issue_key is None:
        ret_status = Ret.CODE.RET_ERROR_CREATING_TICKET_FAILED

    else:
        printer.print_info('Your ticket has been created with key:', issue_key)

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
