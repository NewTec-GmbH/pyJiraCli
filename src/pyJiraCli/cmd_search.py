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
import json
import argparse

from pyJiraCli.jira_server import Server
from pyJiraCli.file_handler import FileHandler as File
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
def register(subparser) -> argparse.ArgumentParser:
    """ Register subparser commands for the login module.
        
    Args:
        subparser (obj):   the command subparser provided via __main__.py
        
    Returns:
        obj:    the command parser of this module
    """
    # subparser for the 'search' command
    sub_parser_search : argparse.ArgumentParser = subparser.add_parser('search',
                                      help="Search for the Jira server for issues \
                                            using the specified filter string.")

    sub_parser_search.add_argument('filter',
                            type=str,
                            help="Filter string to search for. Must be in JQL format.")

    sub_parser_search.add_argument('--max',
                            type=int,
                            metavar='<MAX>',
                            help="Maximum number of issues that may be found. Default is 50.")

    sub_parser_search.add_argument('--save',
                            type=str,
                            metavar='<PATH TO FILE>',
                            help="Absolute filepath or filepath relative " + \
                                 "to the current work directory to a JSON file.")

    return sub_parser_search

def execute(args) -> Ret.CODE:
    """ This function servers as entry point for the command 'search'.
        It will be stored as callback for this modules subparser command.
    
    Args: 
        args (obj): The command line arguments.
        
    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """
    return _cmd_search(args.filter, args.profile, args.max, args.save)

def _cmd_search(filter_str:str, profile_name:str, results:int, save_file:str) -> Ret.CODE:
    """ Search tickets with a provided filter or search string.
    
    Args:
        filter_str (str):   String containing the search parameters.
        profile_name (str): The server profile that shall be used.
        results (int):      The maximum number of search results.
        save_file (str):    The absolute filepath or a relative filepath to the current
                            work directory to a JSON file, where the search will be stored. 
        
    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """
    ret_status = Ret.CODE.RET_OK
    server = Server()
    printer = Printer()

    if results is None:
        results=50

    ret_status = server.login(profile_name)

    if ret_status == Ret.CODE.RET_OK:
        ret_status = server.search(filter_str, results)

    if ret_status == Ret.CODE.RET_OK:
        found_issues = server.get_search_result()
        printer.print_info('Search string:', filter_str)
        printer.print_info('Found Issues:', str(len(found_issues)))

        if save_file is not None:

            search_dict = {
                'profile' : profile_name,
                'search'  : filter_str,
                'max'     : results,
                'found'   : len(found_issues)
            }

            issue_list = []

            for issue in found_issues:
                issue_list.append(issue.raw)

            search_dict['issues'] = issue_list

            ret_status = _save_search(save_file, search_dict)

        else:
            _print_table(found_issues)

    return ret_status

def _print_table(issues:list) -> None:
    """ Print a quick overview for all issues in the list.

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


def _save_search(save_file:str, search_dict:dict) -> Ret.CODE:
    """ Save the search result to a JSON file.

    Args:
        save_file (str): The filepath to the JSON file.
        search_dict (dict): The dictionary with the search data.

    Returns:
        Ret.CODE: _description_
    """
    ret_status = Ret.CODE.RET_OK

    file = File()
    _printer = Printer()

    write_data = json.dumps(search_dict, indent=4)

    ret_status = file.set_filepath(save_file)

    if ret_status == Ret.CODE.RET_OK:
        ret_status = file.write_file(write_data)

    if ret_status == Ret.CODE.RET_OK:
        _printer.print_info("Search was saved in file:", save_file)

    return ret_status
