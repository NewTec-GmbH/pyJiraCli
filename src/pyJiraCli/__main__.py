"""The main module with the program entry point."""

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
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICU5LAR PURPOSE ARE
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

import sys
import argparse
from colorama import just_fix_windows_console

# Import command modules
from pyJiraCli import cmd_import
from pyJiraCli import cmd_export
from pyJiraCli import cmd_search
from pyJiraCli import cmd_print
from pyJiraCli import cmd_profile

from pyJiraCli.printer import Printer, PrintType
from pyJiraCli.ret import Ret
from pyJiraCli.version import __version__, __author__, __email__, __repository__, __license__

################################################################################
# Variables
################################################################################

# Add command modules here
_CMD_MODULS = [
    cmd_export,
    cmd_import,
    cmd_search,
    cmd_print,
    cmd_profile
]

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################


def add_parser() -> argparse.ArgumentParser:
    """ Add parser for command line arguments and
        set the execute function of each 
        cmd module as callback for the subparser command.
        Return the parser after all the modules have been registered
        and added their subparsers.


    Returns:
        obj:  The parser object for commandline arguments.
    """
    parser = argparse.ArgumentParser(prog='pyJiraCli',
                                     description="A CLI tool to import and export Jira issues \
                                                  between server and JSON files.",
                                     epilog="Copyright (c) 2024 NewTec GmbH - " +
                                     __license__ +
                                     " - Find the project on GitHub: " + __repository__)

    parser.add_argument('--profile',
                        type=str,
                        metavar='<server profile>',
                        help="The name of the server profile which shall be used for this process")

    parser.add_argument("--version", "-v",
                        action="version",
                        version="%(prog)s " + __version__)

    parser.add_argument("--verbose",
                        action="store_true",
                        help="Print full command details before executing the command.\
                            Enables logs of type INFO and WARNING.")

    subparser = parser.add_subparsers(required='True')

    # Register command modules und argparser arguments
    for mod in _CMD_MODULS:
        cmd_parser = mod.register(subparser)
        cmd_parser.set_defaults(func=mod.execute)

    return parser


def main() -> Ret.CODE:
    """ The program entry point function.

    Returns:
        int: System exit status.
    """
    ret_status = Ret.CODE.RET_OK
    printer = Printer()
    args = None

    # Get all arguments except the program name.
    input_arguments = sys.argv[1:]

    # If no arguments are given, show help. Required by Python 3.8.
    if 0 == len(input_arguments):
        input_arguments.append("--help")

    # Older windows consoles doesn't support ANSI color codes by default.
    # Enable the Windows built-in ANSI support.
    just_fix_windows_console()

    # Get parser
    parser = add_parser()

    args = parser.parse_args(input_arguments)

    assert args is not None
    assert args.func is not None

    # In verbose mode print all program arguments
    if args.verbose:
        printer.set_verbose()
        print("Program arguments: ")

        for arg in vars(args):
            print(f"* {arg} = {vars(args)[arg]}")
        print("\n")

    # call command function and return exit status
    ret_status = args.func(args)

    if ret_status != Ret.CODE.RET_OK:
        printer.print_error(PrintType.ERROR, ret_status)

    return ret_status

################################################################################
# Main
################################################################################


if __name__ == "__main__":
    sys.exit(main())
