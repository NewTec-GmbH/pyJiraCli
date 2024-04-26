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
# subparser for the 'import' command
def register(subparser):
    """ Register subparser commands for the import module.
        
    Args:
        subparser (obj):  the command subparser provided via __main__.py
        
    Returns:
        obj:  the commmand parser of this module
    """
    sb_import = subparser.add_parser('import',
                                      help="import jira issue from json or csv file")

    sb_import.add_argument('file',
                            type=str,
                            help="file path to the json file")

    return sb_import

def execute(args) -> Ret:
    """ Execute the import command function.
    
    Args: 
        args:   the command line arguments
        
    Returns:
        Ret:   Ret.RET_OK if succesfull, corresponding error code if not
    """
    ret_status = Ret.RET_OK

    ret_status =  _cmd_import(args.file, args.user, args.pw)

    return ret_status

def _cmd_import(input_file:str, user:str, pw:str) -> Ret:
    """ Import a jira issue from a json or csv file.
        Create a jira issue on the server with the data
        read from the input file.
    
    Args:
        input_file (str):  the filepath to the input file
        user (str):        username for login
        pw (str):          password for login
        
    Returns:
        Ret:   Ret.RET_OK if succesfull, corresponding error code if not
    """
    ret_status = Ret.RET_OK
    issue = JiraIssue()
    server = Server()
    issue_dict = {}

    file = File()

    # check if provided file is viable
    ret_status = file.set_filepath(input_file)

    if ret_status == Ret.RET_OK:
        if file.get_file_extension() not in ('.json', '.csv'):
            ret_status = Ret.RET_ERROR_WORNG_FILE_FORMAT
    else:
        ret_status = Ret.RET_ERROR_FILE_NOT_FOUND

    # if file is viable
    if ret_status == Ret.RET_OK:

        ret_status = file.open_file(file_mode='r')

    if ret_status == Ret.RET_OK:
        issue_dict = _read_file(file)

        issue.import_issue(issue_dict)

    if ret_status == Ret.RET_OK:
        ret_status = server.login(user, pw)

        if ret_status == Ret.RET_OK:
            jira = server.get_handle()
            ret_status = issue.create_ticket(jira)

    return ret_status


def _read_file(file:File) -> dict:
    """ Read in the data from a json or csv file.

    Args:
        file (FileHandler): the file handler for the input file
    
    Returns:
        dict:  the dictionary with file informations   
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
