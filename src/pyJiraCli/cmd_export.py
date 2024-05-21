""" Command to export tickets from jira.
    Issues will be loaded from the server
    and written to a json or csv file.
    The file location or file can be provided.
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
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL-
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

################################################################################
# Imports
################################################################################
import os

from pyJiraCli.jira_issue import JiraIssue
from pyJiraCli.jira_server import Server
from pyJiraCli.printer import Printer, PrintType
from pyJiraCli.ret import Ret, Warnings
################################################################################
# Variables
################################################################################
printer = Printer()
################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################
def register(subparser) -> object:
    """ Register the subparser commands for the export module.
        
    Args:
        subparser (obj):   The command subparser object provided via __main__.py.
        
    Returns:
        obj:    The commmand parser obj of this module.
    """

    sb_export = subparser.add_parser('export',
                                      help="export jira issue to json file")

    sb_export.add_argument('issue',
                           type=str,
                           help="issue key")

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

def execute(args) -> Ret:
    """ This function servers as entry point for the command 'export'.
        It will be stored as callback for this moduls subparser command.
    
    Args: 
        args (obj): The command line arguments.
        
    Returns:
        Ret:   Returns Ret.RET_OK if successful or else the corresponding error code.
    """
    return _cmd_export(args)

# export command function
def _cmd_export(args) -> Ret:
    """ Export a jira ticket to a json or csv file.

        The function takes the commandline arguments and extracts the
        provided filepath from -path -file and -csv option.

        If the option -file (filename) is not provided, the function will 
        take the issue key as filename.

        If the issue is valid, the issue data will be read from the server and stored
        in an instance of the JiraIssue class.

        Lastly the data will be written and stored in a json or csv file 
        depending on if the -csv option was set or not.
    
    Args:
        args (obj): The command line arguments.
        
    Returns:
        Ret:   Returns Ret.RET_OK if successful or else the corresponding error code.
    """

    ret_status = Ret.RET_OK

    filepath = _get_filepath(args.issue,
                             args.file,
                             args.path,
                             args.csv)
    if filepath is None:
        ret_status = Ret.RET_ERROR_FILEPATH_INVALID

    else:
        ret_status = _export_ticket_to_file(args.issue,
                                            filepath,
                                            args.user,
                                            args.pw)

    if ret_status == Ret.RET_OK:
        printer.print_info('File saved at:', filepath)

    return ret_status


def _get_filepath(issue:str, file:str, path:str, csv:bool) -> str:
    """ Put together the output file path.
        If no filename was provided with file option, 
        the issue key will be used as filename.
        The file extension (json/csv) will be set according to csv option.
       
    Args:
        issue (str): The issue key (used as filename if no name or file provided).
        file (str):  The filename for the file which will be created.
        path (str):  Path to the folder where the file shall be stored.
        csv (bool):  Flag, if true save the file in csv format.

    Returns:
        str:   Path where the ticket file will be stored or None.
    """
    file_path = None

    if file is None:
        filename = issue
    else:
        filename, csv = _process_file_option(file, csv)

    if path is None:
        # save file in project folder

        path_comps = filename.split('/')

        if len(path_comps) == 1:
            path_comps = filename.split('\\')

        if len(path_comps) > 1:
            if -1 == path_comps[0].find('\\'):
                path_comps[0] += '\\'

            file_path = os.path.join(*path_comps)

            if csv:
                file_path = f'{file_path}.csv'
            else:
                file_path = f'{file_path}.json'

        else:
            if csv:
                file_path = f'.\\{filename}.csv'
            else:
                file_path = f'.\\{filename}.json'

    else:
        # check if provided path or file is viable
        file_path = _get_path(path, filename, file, csv)

    return file_path

def _export_ticket_to_file(issue_key:str, filepath:str, user:str, pw:str) -> Ret:
    """ Export a jira issue from the server
        and write the issue data to a csv or json file.
        
    Args:
        issue_key (str):  The issue key as a string.
        filepath (str):   The path to the output file.
        user (str):       User name for login (if provided).
        pw (str):         Password for login (if provided).  

    Returns:
        Ret:   Returns Ret.RET_OK if successful or else the corresponding error code.
    """
# pylint: disable=R0801
    ret_status = Ret.RET_OK
    issue = JiraIssue()
    server = Server()

    # login to server, get jira handle obj
    ret_status = server.login(user, pw)

    if ret_status == Ret.RET_OK:
        jira = server.get_handle()
        # export issue from jira server
        ret_status = issue.export_issue(jira, issue_key)
# pylint: enable=R0801

    csv = False

    if os.path.splitext(filepath)[-1] == '.csv':
        csv = True

    if ret_status == Ret.RET_OK:
        if csv:
            # export fiel to csv format
            ret_status = issue.create_csv(filepath)

        else:
            # export file to json format
            ret_status = issue.create_json(filepath)

    server.logout()

    return ret_status

def _process_file_option(file:str, csv:bool) -> tuple[str, bool]:
    """ Get the filename. Handle possible extension errors 
        with the file provided via the -file option.
        The returned filename will be without extension.

    Args:
        file (str): The -file option string provided via the console.

    Returns:
        tuple[str, bool]:   str:  The filename according to the -file option.
                                  The extension will be added later.
                            bool: The new csv flag, The flag can change,
                                  if it doesnt match the provided filename.
    """
    # check for file extension
    ext = os.path.splitext(file)[-1]

    if len(ext) == 0:
        filename = file

    else:
        if ext == '.json' and csv:
            printer.print_error(PrintType.WARNING, Warnings.WARNING_CSV_OPTION_WRONG )
            csv = False

        elif ext == '.csv' and not csv:
            printer.print_error(PrintType.WARNING, Warnings.WARNING_CSV_OPTION_WRONG )
            csv = True

        elif ext[0] == '.' and \
             ext not in ('.json', '.csv'):
            printer.print_error(PrintType.WARNING, Warnings.WARNING_UNKNOWN_FILE_EXTENSION)

    filename = file.replace(ext, '')

    return filename, csv


def _get_path(path:str, filename:str, file:str, csv:bool) -> str:
    """ Get the path to the output file with 
        the provided -file and -path options.

    Args:
        path (str): The path provided by the -path option.
        filename (str): the filename that was returned by _process_file_option().
        file (str): The file provided by the -file option.
        csv (bool): The csv flag entered with the -csv option.

    Returns:
        str: The final path where the output file will be stored. 
    """
    if os.path.exists(path):

        # check if its a path to a file or a folderss
        if os.path.isfile(path):
            file_path = _handle_path_to_file(path, filename, file, csv)

        else:
            # folder to save files was provided
            if csv:
                file_path = os.path.join(path, f'{filename}.csv')
            else:
                file_path = os.path.join(path, f'{filename}.json')

        file_path_comps = file_path.split('/')

        if len(file_path_comps) > 1:

            if -1 == file_path_comps[0].find('\\'):
                file_path_comps[0] += '\\'
                file_path = os.path.join(*file_path_comps)

    else:
        file_path = None

    return file_path

def _handle_path_to_file(path:str, filename:str, file:str, csv:bool) -> str:
    """ Handle the output file path if a file location
        was provided with the -path option.

    Args:
        path (str): The path provided by the -path option.
        filename (str): the filename that was returned by _process_file_option().
        file (str): The file provided by the -file option.
        csv (bool): The csv flag entered with the -csv option.

    Returns:
        str: Returns the file path is a path was provided with the -file option.
    """

    # check for file extension
    ext = os.path.splitext(path)[-1]

    file_path = None

    if ext == '.json' and csv or \
       ext == '.csv' and not csv:
        printer.print_error(PrintType.WARNING, Warnings.WARNING_CSV_OPTION_WRONG)
        file_path = path
        csv = ext == '.csv'

    if ext not in ('.json', '.csv'):
        printer.print_error(PrintType.WARNING, Warnings.WARNING_UNKNOWN_FILE_EXTENSION)
        path.replace(ext, '')

        if csv:
            file_path = os.path.join(path, f'{filename}.csv')
        else:
            file_path = os.path.join(path, f'{filename}.json')

    else:
        file_path = path

    if file is not None:
        path_comps = path.split('/')

        if len(path_comps) > 1:
            if -1 == path_comps[0].find('\\'):
                path_comps[0] += '\\'

            if csv:
                file_path = os.path.join(*path_comps[:-1], f'{filename}.csv')
            else:
                file_path = os.path.join(*path_comps[:-1], f'{filename}.json')

    return file_path
