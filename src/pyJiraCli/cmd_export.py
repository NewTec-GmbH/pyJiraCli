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

# subparser for the 'export'command
def register(subparser):
    """ register subparser commands for the export module
        
        param:
        subparser: subparser
        
        return:
        commmand parser of this module
    """

    sb_export = subparser.add_parser('export',
                                      help="export jira issue to json file")

    sb_export.add_argument('issue',
                           type=str,
                           help="issue key")

    sb_export.add_argument('-user',
                            type=str,
                            metavar='<username>',
                            help="jira username if not provided with login")

    sb_export.add_argument('-pw'  ,
                            type=str,
                            metavar='<password>',
                            help="jira password if not provided with login")

    sb_export.add_argument('-path',
                            type=str,
                            metavar='<folder_path>',
                            help="Destination for the output file")

    sb_export.add_argument('-file',
                            type=str,
                            metavar='<filename>',
                            help="name of the output file")

    sb_export.add_argument('-csv' ,
                            action='store_true',
                            help="save data in csv file format")

    return sb_export

def execute(args):
    """execute command function"""
    return _cmd_export(args)

# export command function
def _cmd_export(args):
    """ export jira ticket to json or csv file
    
        param:
        args: command line arguments from parser
        
        return:
        the status of the module
    """
    
    ret_val = Ret.RET_OK

    filepath, ret_val = _get_filepath(args.issue,
                                      args.file,
                                      args.path,
                                      args.csv)
    if ret_val != Ret.RET_OK:
        return ret_val

    return _export_ticket_to_file(args.issue,
                                  filepath,
                                  args.user,
                                  args.pw,
                                  args.csv)


def _get_filepath(issue, file, path, csv):
    """put together the output file path 
       
       param:
       issue: issue key (used as filename if no name or file provided)
       file:  the filename for the file which will be created
       path:  path to the folder where the file shall be stored
       csv:   flag, if true save the file in csv format

       return:
       the filepath to the ticket file
       return status of the module
       """
    
    if file is None:
        filename = issue
    else:
        filename = file

    if path is None:
        # save file in project folder
        if csv:
            file_path = f'./issues/{filename}.csv'
        else:
            file_path = f'./issues/{filename}.json'

    else:
        # check if provided path or file is viable
        if os.path.exists(path):

            # check if its a path to a file or a folderss
            if os.path.isfile(path):

                # check for file extension
                ext = os.path.splitext(path)[-1]

                if ext == '.json' and not csv or \
                   ext == '.csv' and csv:
                    file_path = path

                else:
                    return None, Ret.RET_ERROR_WORNG_FILE_FORMAT
            else:
                # folder to save files was provided
                if csv:
                    file_path = os.path.join(path, f'{filename}.csv')
                else:
                    file_path = os.path.join(path, f'{filename}.json')
        else:
            return None, Ret.RET_ERROR_FILE_NOT_FOUND

    return file_path, Ret.RET_OK

def _export_ticket_to_file(issue, filepath, user, pw, csv):
    """"export jira issue from server to json or csv file
        
        param:
        issue:     issue key
        filepath:  path to the output file
        user:      user name for login (if provided)
        pw:        password (if provided)  
        csv:       flag, if true save the file in csv format

        return:
        return status of the module
    """

    ret_status = Ret.RET_OK

    issue = jira_issue.JiraIssue()

    # login to server, get jira handle obj
    jira, ret_status = server.login(user, pw)

    if ret_status != Ret.RET_OK:
        return ret_status

    # export issue from jira server
    ret_status = issue.export_issue(jira, issue)

    if ret_status != Ret.RET_OK:
        return ret_status

    if csv:
        # export fiel to csv format
        ret_status = issue.create_csv(filepath)

    else:
        # export file to json format
        ret_status = issue.create_json(filepath)

    return ret_status