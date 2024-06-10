""" Command to export tickets from jira.
    Issues will be loaded from the server
    and written to a JSON or csv file.
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
import json
import argparse

from pyJiraCli.jira_server import Server
from pyJiraCli.file_handler import FileHandler as File
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
def register(subparser) -> argparse.ArgumentParser:
    """ Register the subparser commands for the export module.
        
    Args:
        subparser (obj):   The command subparser object provided via __main__.py.
        
    Returns:
        obj:    The commmand parser obj of this module.
    """

    sub_parser_export: argparse.ArgumentParser = subparser.add_parser('export',
                                     help="Export a ticket from a Jira Server to a JSON file.")

    sub_parser_export.add_argument('issue',
                           type=str,
                           help="Jira issue key")

    sub_parser_export.add_argument('--path',
                           type=str,
                           metavar='<folder_path>',
                           help="Destination folder for the output file. \
                                Folder must exist.")

    sub_parser_export.add_argument('--filename',
                           type=str,
                           metavar='<filename>',
                           help="Name of the output file. Default is the issue key.")

    sub_parser_export.add_argument('--csv',
                           action='store_true',
                           help="Save data in CSV file format.")

    return sub_parser_export

def execute(args) -> Ret.CODE:
    """ This function servers as entry point for the command 'export'.
        It will be stored as callback for this moduls subparser command.
    
    Args: 
        args (obj): The command line arguments.
        
    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """
    return _cmd_export(args)

# export command function
def _cmd_export(args) -> Ret.CODE:
    """ Export a jira ticket to a JSON or csv file.

        The function takes the commandline arguments and extracts the
        provided filepath from -path -file and -csv option.

        If the option -file (filename) is not provided, the function will 
        take the issue key as filename.

        The data will be written and stored in a JSON or csv file 
        depending on if the -csv option was set or not.
    
    Args:
        args (obj): The command line arguments.
        
    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """

    ret_status = Ret.CODE.RET_OK

    filepath = _get_filepath(args.issue,
                             args.filename,
                             args.path,
                             args.csv)
    if filepath is None:
        ret_status = Ret.CODE.RET_ERROR_FILEPATH_INVALID

    else:
        ret_status = _export_ticket_to_file(args.issue,
                                            filepath,
                                            args.profile)

    if ret_status == Ret.CODE.RET_OK:
        printer.print_info('File saved at:', filepath)

    return ret_status


def _get_filepath(issue:str, arg_file:str, arg_path:str, csv:bool) -> str:
    """ Put together the output file path.
        If no filename was provided with file option, 
        the issue key will be used as filename.
        The file extension (json/csv) will be set according to csv option.
       
    Args:
        issue (str):     The issue key (used as filename if no name or file provided).
        arg_file (str):  The -file argument from the command line.
        arg_path (str):  The -path argument from the dommand line.
        csv (bool):      Flag, if true save the file in csv format.

    Returns:
        str:   Path where the ticket file will be stored or None.
    """
    file_path = None

    if arg_file is None:
        filename = issue
    else:
        filename, csv = _process_file_argument(arg_file, csv)

    if arg_path is None:
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
        file_path = _process_path_argument(arg_path, filename, arg_file, csv)

    return file_path

def _export_ticket_to_file(issue_key:str, filepath:str, profile_name:str) -> Ret.CODE:
    """ Export a jira issue from the server
        and write the issue data to a csv or JSON file.
        
    Args:
        issue_key (str):    The issue key as a string.
        filepath (str):     The path to the output file.
        profile_name (str): The server profile that shall be used.

    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """
# pylint: disable=R0801
    ret_status = Ret.CODE.RET_OK
    server = Server()

    # login to server, get jira handle obj
    ret_status = server.login(profile_name)

    if ret_status == Ret.CODE.RET_OK:
        ret_status = server.search(f"key = {issue_key}", max_results=1)

        if ret_status == Ret.CODE.RET_OK:
            issue = server.get_search_result().pop().raw
# pylint: enable=R0801

    csv = False

    if os.path.splitext(filepath)[-1] == '.csv':
        csv = True

    if ret_status == Ret.CODE.RET_OK:
        if csv:
            # export fiel to csv format
            # csv support will be remove with next bugfix update
            pass

        else:
            file = File()

            # export file to JSON format
            ret_status = file.set_filepath(filepath)
            write_data = json.dumps(issue, indent=4)

            if ret_status == Ret.CODE.RET_OK:
                ret_status = file.write_file(write_data)

    return ret_status

def _process_file_argument(arg_file:str, csv:bool) -> tuple[str, bool]:
    """ Get the filename. Handle possible extension errors 
        with the filename provided via the -file option.
        If a path to a file was supplied, the path will be kept.
        The returned filename will be without extension.

    Args:
        arg_file (str): The -file option string provided via the console.
        csv (bool): The -csv option from the command line arguments.

    Returns:
        Tuple[str, bool]:   str:  The filename according to the -file option.
                                  The extension will be added later.
                            bool: The new csv flag, The flag can change,
                                  if it doesnt match the provided filename.
    """
    # check for file extension
    ext = os.path.splitext(arg_file)[-1]

    if len(ext) == 0:
        filename = arg_file

    else:
        if ext == '.json' and csv:
            printer.print_error(PrintType.WARNING, Warnings.CODE.WARNING_CSV_OPTION_WRONG )
            csv = False

        elif ext == '.csv' and not csv:
            printer.print_error(PrintType.WARNING, Warnings.CODE.WARNING_CSV_OPTION_WRONG )
            csv = True

        elif ext[0] == '.' and \
             ext not in ('.json', '.csv'):
            printer.print_error(PrintType.WARNING, Warnings.CODE.WARNING_UNKNOWN_FILE_EXTENSION)

    filename = arg_file.replace(ext, '')

    return filename, csv


def _process_path_argument(arg_path:str, filename:str, arg_file:str, csv:bool) -> str:
    """ Get the path to the output file with 
        the provided -file and -path options.
        If the -file argument provides a path too, 
        the path from the -path option will be used,
        in combination with the filename from the
        -file option. 

    Args:
        arg_path (str): The path provided by the -path option.
        filename (str): the filename that was returned by _process_file_argument().
        arg_file (str): The file provided by the -file option.
        csv (bool): The csv flag entered with the -csv option.

    Returns:
        str: The final path where the output file will be stored. 
    """
    if os.path.exists(arg_path):

        # check if its a path to a file or a folderss
        if os.path.isfile(arg_path):
            file_path = _handle_path_to_file(arg_path, filename, arg_file, csv)

        else:
            # folder to save files was provided
            if csv:
                file_path = os.path.join(arg_path, f'{filename}.csv')
            else:
                file_path = os.path.join(arg_path, f'{filename}.json')

        file_path_comps = file_path.split('/')

        if len(file_path_comps) > 1:

            if -1 == file_path_comps[0].find('\\'):
                file_path_comps[0] += '\\'
                file_path = os.path.join(*file_path_comps)

    else:
        file_path = None

    return file_path

def _handle_path_to_file(arg_path:str, filename:str, arg_file:str, csv:bool) -> str:
    """ Process the final filepath if both the -path argument contains a file.
        If the file is viable and no filename was provided via the -file argument, 
        the file will from -path will be used.
        If a filename is supplied with -file, the filename in the -path folder
        will be replaced with the filename from the
        -file argument.

    Args:
        arg_path (str): The path provided by the -path option.
        filename (str): the filename that was returned by _process_file_argument().
        arg_file (str): The file provided by the -file option.
        csv (bool): The csv flag entered with the -csv option.

    Returns:
        str: Returns the final filepath after the command arguments have been processed.
    """

    # check for file extension
    ext = os.path.splitext(arg_path)[-1]

    file_path = None

    if ext == '.json' and csv or \
       ext == '.csv' and not csv:
        printer.print_error(PrintType.WARNING, Warnings.CODE.WARNING_CSV_OPTION_WRONG)
        file_path = arg_path
        csv = ext == '.csv'

    if ext not in ('.json', '.csv'):
        printer.print_error(PrintType.WARNING, Warnings.CODE.WARNING_UNKNOWN_FILE_EXTENSION)
        arg_path.replace(ext, '')

        if csv:
            file_path = os.path.join(arg_path, f'{filename}.csv')
        else:
            file_path = os.path.join(arg_path, f'{filename}.json')

    else:
        file_path = arg_path

    if arg_file is not None:
        path_comps = arg_path.split('/')

        if len(path_comps) > 1:
            if -1 == path_comps[0].find('\\'):
                path_comps[0] += '\\'

            if csv:
                file_path = os.path.join(*path_comps[:-1], f'{filename}.csv')
            else:
                file_path = os.path.join(*path_comps[:-1], f'{filename}.json')

    return file_path
