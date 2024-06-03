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
from pyJiraCli.jira_server import Server
from pyJiraCli.printer import Printer
from pyJiraCli.ret import Ret
################################################################################
# Variables
################################################################################

HEADER = ['Key', 'Project', 'Summary', 'Created', 'Creator']

HEADER_COL_WIDTH = {
    'Key'     : 22,
    'Project' : 18,
    'Summary' : 50,
    'Created' : 12,
    'Creator' : 15
}

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################
def register(subparser) -> object:
    """ Register subparser commands for the login module.
        
    Args:
        subparser (obj):   the command subparser provided via __main__.py
        
    Returns:
        obj:    the commmand parser of this module
    """
    # subparser for the 'search' command
    sb_search = subparser.add_parser('search',
                                      help="Search for the Jira server for issues \
                                            using the specified filter string.")

    sb_search.add_argument('filter',
                            type=str,
                            help="Filter string to search for. Must be in JQL format.")

    sb_search.add_argument('--max',
                            type=int,
                            metavar='<MAX>',
                            help="Maximum number of issues that may be found. Default is 50.")

    return sb_search

def execute(args) -> Ret:
    """ This function servers as entry point for the command 'search'.
        It will be stored as callback for this moduls subparser command.
    
    Args: 
        args (obj): The command line arguments.
        
    Returns:
        Ret:   Returns Ret.RET_OK if successful or else the corresponding error code.
    """
    return _cmd_search(args.filter, args.user, args.password, args.max)

def _cmd_search(filter_str:str, user:str, pw:str, results:int) -> Ret:
    """ Search tickets with a provided filter or search string.
    
    Args:
        filter_str (str):   String containing the search parameters.
        user (str):         Username for login.
        pw (str)            Password for login.
    
    Returns:
        Ret:   Returns Ret.RET_OK if successful or else the corresponding error code.
    """
    ret_status = Ret.RET_OK
    server = Server()
    printer = Printer()

    if results is None:
        results=50

    ret_status = server.login(user, pw)

    if ret_status == Ret.RET_OK:
        ret_status = server.search(filter_str, results)

    if ret_status == Ret.RET_OK:
        found_issues = server.get_search_result()
        printer.print_info('Search string:', filter_str)
        printer.print_info('Found Issues:', str(len(found_issues)))

        _print_table(found_issues)

    server.logout()

    return ret_status

def _print_table(issues:list):
    """ Print a quick overview vor all issues in the list.

    Args:
        issues (list): list with all found issues
    """
    for header in HEADER:
        print(f"{header:<{HEADER_COL_WIDTH[header]}}", end="")
    print()

    for issue in issues:
        print(f"{issue.key:<{HEADER_COL_WIDTH['Key']}}", end="")
        print(f"{issue.fields.project.key:<{HEADER_COL_WIDTH['Project']}}", end="")
        print(f"{issue.fields.summary[:HEADER_COL_WIDTH['Summary'] - 2]:<{HEADER_COL_WIDTH['Summary']}}", end="") # pylint: disable=line-too-long
        print(f"{issue.fields.created[:10]:<{HEADER_COL_WIDTH['Created']}}", end="")
        print(f"{issue.fields.creator.name:<{HEADER_COL_WIDTH['Creator']}}", end="\n")
