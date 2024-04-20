"""Command for the import function.
   imports ticket information from a json or csv file
   and writes the imported data to a jira ticket"""

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

# from pyJiraCli
from pyJiraCli import jira_issue
from pyJiraCli import jira_server as server
from pyJiraCli.retval import Ret
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
    """register subparser commands for the import module
    
        param:
        subparser: subparser
        
        return:
        commmand parser of this module
    """

    sb_import = subparser.add_parser('import',
                                      help="import jira issue from json or csv file")

    sb_import.add_argument('file',
                            type=str,
                            help="file path to the json file")

    sb_import.add_argument('-user',
                            type=str,
                            metavar='<username>',
                            help="jira username if not provided with set_login")

    sb_import.add_argument('-pw',
                            type=str,
                            metavar='<password>',
                            help="jira password if not provided with set_login")

    return sb_import

def execute(args):
    """execute command function"""
    return _cmd_import(args)

def _cmd_import(args):
    """import jira issue from json or csv file
    
        param:
        args: the commandline arguments
        
        return:
        the status of the module
    """

    file = args.file
    user = args.user
    pw   = args.pw

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
            return Ret.RET_ERROR_WORNG_FILE_FORMAT
    else:
        return Ret.RET_ERROR_FILE_NOT_FOUND

    if ext == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            issue_dict = json.load(f)

    if ext == '.csv':
        with open(file_path, 'r', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f, delimiter=';')

            for row in csv_reader:
                issue_dict = row

    issue.import_issue(issue_dict)

    jira, ret_status = server.login(user, pw)

    if ret_status != Ret.RET_OK:
        return ret_status

    ret_status = issue.create_ticket(jira)

    return ret_status