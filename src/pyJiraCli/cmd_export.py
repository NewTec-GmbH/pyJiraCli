"""Command to export tickets from jira.
   issues will be loaded from the server
   and written to a json or csv file
   the file location or file can be provided"""

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

import jira_issue
import jira_server as server
from retval import Ret

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

# subparser for the 'export'command
def add_parser(subparser):
    """register subparser commands for the export module"""
    sb_export = subparser.add_parser('export', help="export jira issue to json file")
    sb_export.add_argument('issue', type=str, help="issue key")
    sb_export.add_argument('-user', type=str, help="jira usertname if not provided with set_login")
    sb_export.add_argument('-pw', type=str, help="jira password if not provided with set_login")
    sb_export.add_argument('-dest', type=str, help="Destination for the output file")
    sb_export.add_argument('-csv',  action='store_true', help="save data in csv file format")
    sb_export.set_defaults(func=export_data)

# export command function
def export_data(args):
    """"export jira issue from server to json file"""
    ret_status = Ret.RET_OK

    issue = jira_issue.JiraIssue()

    # login to server, get jira handle obj
    jira, ret_status = server.login(args.user, args.pw)

    if ret_status != Ret.RET_OK:
        return ret_status

    # export issue from jira server
    ret_status = issue.export_issue(jira, args.issue)

    if ret_status != Ret.RET_OK:
        return ret_status

    if args.dest is None:
        # save file in project folder
        if args.csv:
            file_path = f'{issue.get_key()}.csv'
        else:
            file_path = f'{issue.get_key()}.json'

    else:
        # check if provided path or file is viable
        if os.path.exists(args.dest):

            # check if its a path to a file or a folderss
            if os.path.isfile(args.dest):

                # check for file extension
                ext = os.path.splitext(args.dest)[-1]

                if ext == '.json' and not args.csv or \
                   ext == '.csv' and args.csv:
                    file_path = args.dest

                else:
                    return Ret.RET_ERROR_WORNG_FILE_FORMAT
            else:
                # folder to save files was provided
                if args.csv:
                    file_path = os.path.join(args.dest, f'{issue.get_key()}.csv')
                else:
                    file_path = os.path.join(args.dest, f'{issue.get_key()}.json')
        else:
            return Ret.RET_ERROR_FILE_NOT_FOUND

    if args.csv:
        # export fiel to csv format
        ret_status = issue.create_csv(file_path)

    else:
        # export file to json format
        ret_status = issue.create_json(file_path)

    return ret_status
