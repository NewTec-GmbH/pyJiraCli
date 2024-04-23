"""Command to search for Jira tickets on the provided server.
   searches for tickets by filter or search str provided via the command line
   prints all found ticket keys to command line"""

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
from pyJiraCli import jira_server as server
from pyJiraCli.retval import Ret
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
def register(subparser):
    """add_parser subparser commands for the search module"""
    # subparser for the 'search' command
    sb_search = subparser.add_parser('search',
                                      help="search for jira issues \
                                            with specified filter string")

    sb_search.add_argument('filter',
                            type=str,
                            help="filter string according to \
                                  which issue are to be searched")

    sb_search.add_argument('-max',
                            type=int,
                            help="max number of entries")

    return sb_search

def execute(args):
    """execute command function"""
    return _cmd_search(args.filter, args.user, args.pw, args.max)

def _cmd_search(filter_str, user, pw, results):
    """ search tickets with a provided filter or search string

    param:
    filer_str  the filter string by which issues are searched
    user       username for login
    pw         password for login
    results    max number of results

    return:
    exit status of the module
    """

    ret_status = Ret.RET_OK

    if results is None:
        results=50

    jira, ret_status = server.login(user, pw)

    if ret_status != Ret.RET_OK:
        return ret_status

    found_issues = jira.search_issues(filter_str, maxResults=results)

    print(f'\nSearch string: "{filter_str}"')
    print(f"Found Issues: {len(found_issues)}\n")

    _print_table(found_issues)

    return ret_status

def _print_table(issues):
    for header in HEADER:
        print(f"{header:<{HEADER_COL_WIDTH[header]}}", end="")
    print()

    for issue in issues:
        print(f"{issue.key:<{HEADER_COL_WIDTH['Key']}}", end="")
        print(f"{issue.fields.project.key:<{HEADER_COL_WIDTH['Project']}}", end="")
        print(f"{issue.fields.summary[:HEADER_COL_WIDTH['Summary'] - 2]:<{HEADER_COL_WIDTH['Summary']}}", end="") # pylint: disable=line-too-long
        print(f"{issue.fields.created[:10]:<{HEADER_COL_WIDTH['Created']}}", end="")
        print(f"{issue.fields.creator.name:<{HEADER_COL_WIDTH['Creator']}}", end="\n")
