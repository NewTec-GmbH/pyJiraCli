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
from pyJiraCli import cmd_get_sprints

from pyJiraCli.printer import Printer
from pyJiraCli.ret import Ret
from pyJiraCli.version import __version__, __author__, __email__, __repository__, __license__

################################################################################
# Variables
################################################################################

# Add command modules here
_CMD_MODULES = [
    cmd_export,
    cmd_import,
    cmd_search,
    cmd_print,
    cmd_profile,
    cmd_get_sprints
]

PROG_NAME = "pyJiraCli"
PROG_DESC = "A CLI tool to import and export Jira issues between server and JSON files."
PROG_COPYRIGHT = "Copyright (c) 2024 NewTec GmbH - " + __license__
PROG_GITHUB = "Find the project on GitHub: " + __repository__
PROG_EPILOG = PROG_COPYRIGHT + " - " + PROG_GITHUB

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
        obj:  The parser object for command line arguments.
    """
    parser = argparse.ArgumentParser(prog=PROG_NAME,
                                     description=PROG_DESC,
                                     epilog=PROG_EPILOG)

    parser.add_argument("--version",
                        action="version",
                        version="%(prog)s " + __version__)

    parser.add_argument("-v",
                        "--verbose",
                        action="store_true",
                        help="Print full command details before executing the command.\
                            Enables logs of type INFO and WARNING.")

    subparser = parser.add_subparsers(required='True')

    # Register command modules und argparser arguments
    for mod in _CMD_MODULES:
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

    # Older windows consoles doesn't support ANSI color codes by default.
    # Enable the Windows built-in ANSI support.
    just_fix_windows_console()

    # Get parser
    parser = add_parser()

    # Parse command line arguments.
    # If error occurs, exits the program from this point with code 2.
    args = parser.parse_args()

    if args is None:
        ret_status = Ret.CODE.RET_ERROR_ARGPARSE
    else:
        # In verbose mode print all program arguments
        if args.verbose:
            printer.set_verbose()
            print("Program arguments: ")

            for arg in vars(args):
                print(f"* {arg} = {vars(args)[arg]}")
            print("\n")

        # Call command function and return exit status
        ret_status = args.func(args)

    return ret_status

################################################################################
# Main
################################################################################


if __name__ == "__main__":
    sys.exit(main())
