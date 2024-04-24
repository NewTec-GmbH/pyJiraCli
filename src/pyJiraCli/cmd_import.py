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
import os
import json
import csv

from pyJiraCli import jira_issue
from pyJiraCli import jira_server as server
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

def execute(args):
    """ Execute the import command function.
    
    Args: 
        args:   the command line arguments
        
    Returns:
        Ret:   Ret.RET_OK if succesfull, corresponding error code if not
    """
    ret_status = Ret.RET_OK

    ret_status =  _cmd_import(args.file, args.user, args.pw)

    return ret_status

def _cmd_import(file, user, pw):
    """ Import a jira issue from a json or csv file.
        Create a jira issue on the server with the data
        read from the input file.
    
    Args:
        file (str):     the filepath to the input file
        user (str):     username for login
        pw (str):       password for login
        
    Returns:
        Ret:   Ret.RET_OK if succesfull, corresponding error code if not
    """
    ret_status = Ret.RET_OK
    issue = jira_issue.JiraIssue()
    issue_dict = {}

    # check if provided file is viable
    if os.path.exists(file) and \
       os.path.isfile(file):

        # check for file extension
        ext = os.path.splitext(file)[-1]

        if ext in ('.json', '.csv'):
            file_path = file

        else:
            ret_status = Ret.RET_ERROR_WORNG_FILE_FORMAT
    else:
        ret_status = Ret.RET_ERROR_FILE_NOT_FOUND

    if ret_status == Ret.RET_OK:
        try:
            if ext == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    issue_dict = json.load(f)

            if ext == '.csv':
                with open(file_path, 'r', encoding='utf-8') as f:
                    csv_reader = csv.DictReader(f, delimiter=';')

                    for row in csv_reader:
                        issue_dict = row

            issue.import_issue(issue_dict)

        except(OSError,IOError) as e:
            # print exception
            print(e)
            ret_status = Ret.RET_ERROR_FILE_OPEN_FAILED

    if ret_status == Ret.RET_OK:
        jira, ret_status = server.login(user, pw)

        if ret_status == Ret.RET_OK:
            ret_status = issue.create_ticket(jira)

    return ret_status
