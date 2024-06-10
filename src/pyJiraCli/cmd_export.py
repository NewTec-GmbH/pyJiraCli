""" Command to export tickets from jira.
    Issues will be loaded from the server
    and written to a JSON file.
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
LOG = Printer()
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

    sub_parser_export.add_argument('--file',
                           type=str,
                           metavar='<path to file>',
                           help="Absolute file path or filepath relativ " + \
                                "to the current working directory. " + \
                                "The file format must be JSON. "  \
                                "If a different file format is provided, " + \
                                "the file extension will be replaced.")

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
    """ Export a jira ticket to a JSON file.

        The function takes the commandline arguments and extracts the
        provided filepath from -path and -file option.

        If the option -file (filename) is not provided, the function will 
        take the issue key as filename.

        The data will be written and stored in a JSON file.
    
    Args:
        args (obj): The command line arguments.
        
    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """

    ret_status = Ret.CODE.RET_OK

    file = _process_file_argument(args.issue,
                                      args.file)
    if file is None:
        ret_status = Ret.CODE.RET_ERROR_FILEPATH_INVALID

    else:
        ret_status = _export_ticket_to_file(args.issue,
                                            file,
                                            args.profile)

    if ret_status == Ret.CODE.RET_OK:
        LOG.print_info('File saved at:', file.get_path())

    return ret_status

def _export_ticket_to_file(issue_key:str, file:File, profile_name:str) -> Ret.CODE:
    """ Export a jira issue from the server
        and write the issue data to a JSON file.
        
    Args:
        issue_key (str):    The issue key as a string.
        file (File):        The file object for the output file.
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

            write_data = json.dumps(issue, indent=4)

            if ret_status == Ret.CODE.RET_OK:
                ret_status = file.write_file(write_data)

    return ret_status

def _process_file_argument(issue_key:str ,arg_file:str) -> File:
    """ Get the filename. Handle possible extension errors 
        with the filename provided via the -file option.
        If a path to a file was supplied, the path will be kept.
        The returned filename will be without extension.

    Args:
        issue_key (str): The current issue key. 
        arg_file (str):  The -file option string provided via the console.

    Returns:
        File:   The filename according to the -file option.
                                  The extension will be added later.
    """
    ret_status = Ret.CODE.RET_OK
    file = File()

    if arg_file is None:
        ret_status = file.set_filepath(f".\\{issue_key}.json")

    else:
        ret_status = file.set_filepath(arg_file)

        if ret_status == Ret.CODE.RET_OK:
            ext = file.get_file_extension()

            if ext is None:
                ret_status = file.set_filepath(os.path.join(file.get_parent_path(),
                                                            f'{issue_key}.json'))

            elif ext != '.json':
                LOG.print_error(PrintType.WARNING, Warnings.CODE.WARNING_UNKNOWN_FILE_EXTENSION)

                path, ext = os.path.splitext(file.get_path())

                ret_status = file.set_filepath(path + '.json')

            else:
                # file or the parent directory exist and the file has the proper file format
                pass

        if ret_status != Ret.CODE.RET_OK:
            file = None

    return file
