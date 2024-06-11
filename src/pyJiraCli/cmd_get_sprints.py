""" Command for the gte_sprints function.
    Retrieve sprint data for a specific board and store
    it in a JSON file."""
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

from pyJiraCli.printer import Printer
from pyJiraCli.file_handler import FileHandler as File
from pyJiraCli.jira_server import Server
from pyJiraCli.ret import Ret
################################################################################
# Variables
################################################################################
BOARD_KEY = 'board'
SPRINTS_KEY = 'sprints'

printer = Printer()
################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################
def register(subparser) -> argparse.ArgumentParser:
    """ Register subparser commands for the get_sprints module.
        
    Args:
        subparser (obj):   The command subparser object provided via __main__.py.
        
    Returns:
        obj:    The commmand parser object of this module.
    """

    sub_parser_get_sprints : argparse.ArgumentParser = \
        subparser.add_parser('get_sprints',
                             help="Get all sprints in a board and \
                             save the sprint data into a JSON file.")

    sub_parser_get_sprints.add_argument('board',
                                        type=str,
                                        help="The board for which the sprints shall be stored.")

    sub_parser_get_sprints.add_argument('--file',
                                   type=str,
                                   metavar='<path to file>',
                                   help="Absolute file path or filepath relativ " + \
                                        "to the current working directory. " + \
                                        "The file format must be JSON. ")

    return sub_parser_get_sprints

def execute(args) -> Ret.CODE:
    """ This function servers as entry point for the command 'print'.
        It will be stored as callback for this moduls subparser command.
    
    Args: 
        args (obj): The command line arguments.
        
    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """
    return _cmd_get_sprints(args.board, args.profile, args.file)

def _cmd_get_sprints(board_name:str, profile_name:str, filepath:str) -> Ret.CODE:
    """ Load the sprints in the board and store the data in a 
        JSON file.

    Args:
        board_name (str): The unique board name in string format.
        profile_name (str): The server profile that shall be used.
        filepath (str): The absolute filepath or a relative filepath to
                        the current working directory.

    Returns:
        Ret.CODE: The return status of the module.
    """
    ret_status = Ret.CODE.RET_ERROR

    file = File()

    write_dict = _get_sprints(board_name, profile_name)

    if BOARD_KEY in write_dict:
        writeable_board_name =  write_dict[BOARD_KEY].replace(' ', '_').replace(':', '')
        ret_status = file.process_file_argument(f"{writeable_board_name}_Sprints", filepath)

    else:
        ret_status = Ret.CODE.RET_ERROR_BOARD_NOT_FOUND

    if ret_status == Ret.CODE.RET_OK:
        write_data = json.dumps(write_dict, indent=4)
        ret_status = file.write_file(write_data)

    if ret_status == Ret.CODE.RET_OK:
        printer.print_info('File saved at:', file.get_path())

    return ret_status

def _get_sprints(board_name:str, profile_name:str) -> dict:
    """ Retrieve sprint information for a given board and profile.

    Args:
        board_name (str): The name of the board to retrieve sprint information from.
        profile_name (str): The name of the server profile.

    Returns:
        dict: A dictionary containing sprint information for the specified board and profile.
    """

    server = Server()
    jira = None

    write_dict = {}

    ret_status = server.login(profile_name)

    if ret_status == Ret.CODE.RET_OK:
        jira = server.get_handle()

        jira_boards = jira.boards()

        current_board = None

        for board in jira_boards:
            if board.name == board_name:
                current_board  = board
                break

    if ret_status == Ret.CODE.RET_OK and \
       current_board is not None:

        sprints = jira.sprints(current_board.id)

        printer.print_info(
            f"found {len(sprints)} sprints in board {current_board.name}:",
            *[sprint.name for sprint in sprints]
            )

        write_dict = {
            'board' : current_board.name,
            'sprints' : [sprint.raw for sprint in sprints]
        }

    return write_dict
   