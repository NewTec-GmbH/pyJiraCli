""" Command for the get_sprints function.
    Retrieve sprint data for a specific board and store
    it in a JSON file."""
# BSD 3-Clause License
#
# Copyright (c) 2024 - 2025, NewTec GmbH
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

from pyJiraCli.file_helper import FileHelper
from pyJiraCli.printer import Printer, PrintType
from pyJiraCli.jira_server import Server
from pyJiraCli.ret import Ret


################################################################################
# Variables
################################################################################

BOARD_KEY = 'board'
SPRINTS_KEY = 'sprints'
LOG = Printer()


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
        obj:    The command parser object of this module.
    """

    parser = subparser.add_parser(
        'get_sprints',
        help="Get all sprints in a board and save the sprint data into a JSON file."
    )

    parser.add_argument(
        '--profile',
        type=str,
        metavar='<profile>',
        help="The name of the server profile which shall be used for this process."
    )

    parser.add_argument(
        '-u',
        '--user',
        type=str,
        metavar='<user>',
        help="The user to authenticate with the Jira server."
    )

    parser.add_argument(
        '-p',
        '--password',
        type=str,
        metavar='<password>',
        help="The password to authenticate with the Jira server."
    )

    parser.add_argument(
        '-t',
        '--token',
        type=str,
        metavar='<token>',
        help="The token to authenticate with the Jira server."
    )

    parser.add_argument(
        '-s',
        '--server',
        type=str,
        metavar='<server URL>',
        help="The Jira server URL to connect to."
    )

    parser.add_argument(
        'board',
        type=str,
        help="The board for which the sprints shall be stored."
    )

    parser.add_argument(
        '--file',
        type=str,
        metavar='<path to file>',
        help="Absolute file path or filepath relative " +
        "to the current working directory. " +
        "The file format must be JSON. "
    )

    return parser


def execute(args) -> Ret.CODE:
    """ This function servers as entry point for the command 'print'.
        It will be stored as callback for this module's subparser command.

    Args:
        args (obj): The command line arguments.

    Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
    """
    server = Server()
    ret_status = server.login(args.profile,
                              args.server,
                              args.token,
                              args.user,
                              args.password)

    if Ret.CODE.RET_OK != ret_status:
        LOG.print_error(PrintType.ERROR, ret_status)
    else:
        ret_status = _cmd_get_sprints(args.board, args.file, server)

    return ret_status


def _cmd_get_sprints(board_name: str, filepath: str, server: Server) -> Ret.CODE:
    """ Load the sprints in the board and store the data in a
        JSON file.

    Args:
        board_name (str): The unique board name in string format.
        filepath (str): The absolute filepath or a relative filepath to
                        the current working directory.
        server (Server): The server object to interact with the Jira server.

    Returns:
        Ret.CODE: The return status of the module.
    """

    ret_status = Ret.CODE.RET_OK
    write_dict, ret_status = _get_sprints(board_name, server)

    if ret_status == Ret.CODE.RET_OK:
        writeable_board_name = write_dict[BOARD_KEY].replace(
            ' ', '_').replace(':', '')
        ret_status, output_file_path = FileHelper.process_file_argument(
            f"{writeable_board_name}_Sprints", filepath)

        if ret_status == Ret.CODE.RET_OK:
            try:
                with FileHelper.open_file(output_file_path, 'w') as output_file:
                    write_data = json.dumps(write_dict, indent=4)
                    output_file.write(write_data)

                    msg = f"Successfully saved sprint to '{output_file_path}'."
                    LOG.print_info(msg)
                    print(msg)

            except IOError:
                ret_status = Ret.CODE.RET_ERROR_FILEPATH_INVALID

    return ret_status


def _get_sprints(board_name: str, server: Server) -> tuple[dict, Ret.CODE]:
    """ Retrieve sprint information for a given board and profile.

    Args:
        board_name (str): The name of the board to retrieve sprint information from.
        server (Server): The server object to interact with the Jira server.

    Returns:
        dict: A dictionary containing sprint information for the specified board and profile.
    """

    write_dict = {}
    sprints = None
    jira = server.get_handle()

    # get all boards the current user has access to
    all_boards = []
    start_at = 0
    current_board = None

    ret_status = Ret.CODE.RET_ERROR

    while ret_status == Ret.CODE.RET_ERROR:
        jira_boards = jira.boards(startAt=start_at, maxResults=50)

        # search all boards for the one we're looking for
        for board in jira_boards:
            if board.name == board_name:

                # get the board data
                current_board = board
                ret_status = Ret.CODE.RET_OK
                break

        if ret_status != Ret.CODE.RET_OK:
            if len(all_boards) == jira_boards.total:
                ret_status = Ret.CODE.RET_ERROR_BOARD_NOT_FOUND
            else:
                all_boards.extend(jira_boards)
                start_at += 50

    if (ret_status == Ret.CODE.RET_OK) and \
       (current_board is not None):

        write_dict[BOARD_KEY] = current_board.name

        try:
            sprints = jira.sprints(current_board.id)

            LOG.print_info(
                f"found {len(sprints)} sprints in board {current_board.name}:",
                *[sprint.name for sprint in sprints]
            )

        except:  # pylint: disable=W0702
            LOG.print_info("No sprints found or the board doesn't support sprints. Board:",
                           current_board.name)

        if sprints is not None:
            write_dict[SPRINTS_KEY] = [sprint.raw for sprint in sprints]

    return write_dict, ret_status
