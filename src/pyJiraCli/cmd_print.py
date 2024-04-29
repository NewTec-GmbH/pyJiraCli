""" Command for the print function.
    prints the ticket information for a provided issue key
    onto the console."""
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
from pyJiraCli.jira_server import Server
from pyJiraCli.jira_issue import JiraIssue
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
# subparser for the 'print' command
def register(subparser):
    """ Register subparser commands for the print module.
        
    Args:
        subparser (obj):   the command subparser provided via __main__.py
        
    Returns:
        obj:    the commmand parser of this module
    """

    sb_search = subparser.add_parser('print',
                                      help="print issue details to the console")

    sb_search.add_argument('issue',
                            type=str,
                            help="issue key")

    return sb_search

def execute(args) -> Ret:
    """ This function servers as entry point for the command 'print'.
        It will be stored as callback for this moduls subparser command.
    
    Args: 
        args (obj): the command line arguments
        
    Returns:
        Ret:   Ret.RET_OK if succesfull, corresponding error code if not
    """
    return _cmd_print(args.issue, args.user, args.pw)

def _cmd_print(issue_key:str, user:str, pw:str) -> Ret:
    """Load the data of the provided issue key and 
        and print it to the command line.

    Args:
        issue_key (str): the unique issue key in string format
        user (str): username for login
        pw (str): password for login

    Returns:
        retval.Ret: return status of the module
    """
# pylint: disable=R0801
    ret_status = Ret.RET_OK
    issue = JiraIssue()
    server = Server()

    ret_status = server.login(user, pw)
    if ret_status == Ret.RET_OK:
        jira = server.get_handle()
        # export issue from jira server
        ret_status = issue.export_issue(jira, issue_key)
# pylint: enable=R0801

    if ret_status == Ret.RET_OK:
        issue.print_issue()

    return ret_status
