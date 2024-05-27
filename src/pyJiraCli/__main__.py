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

#import cmd_import
#import cmd_export
#import cmd_search
#import cmd_login
#import cmd_print

# import command modules
from pyJiraCli import cmd_import
from pyJiraCli import cmd_export
from pyJiraCli import cmd_search
from pyJiraCli import cmd_login
from pyJiraCli import cmd_delete
from pyJiraCli import cmd_print

from pyJiraCli.printer import Printer, PrintType
from pyJiraCli.ret import Ret
from pyJiraCli.version import __version__, __author__, __email__, __repository__, __license__

################################################################################
# Variables
################################################################################
# add commando modules here
_CMD_MODULS = [
    cmd_export,
    cmd_import,
    cmd_search,
    cmd_login,
    cmd_delete,
    cmd_print
]

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################
def add_parser() -> object:
    """ Add parser for command line arguments and
        set the execute function of each 
        cmd module as callback for the subparser command.
        Return the parser after all the modules have been registered
        and added their subparsers.
        
    Returns:
        obj:  The parser object for commandline arguments.
    """
    parser = argparse.ArgumentParser(prog='pyJiraCli',
                                     description="A CLI tool to imoprt and export Jira Issues \
                                                  between server and json or csv files.",
                                     epilog="Copyright (c) 2024 " + __author__ + " - " + \
                                             __license__ + \
                                            " - Find the project on github: " + __repository__)

    parser.add_argument('-user',
                        type=str,
                        metavar='<username>',
                        help="jira username if not provided with login")

    parser.add_argument('-pw'  ,
                        type=str,
                        metavar='<password>',
                        help="jira password if not provided with login")

    parser.add_argument("--version",
                        action="version",
                        version="%(prog)s " + __version__)

    parser.add_argument("--verbose",
                        action="store_true",
                        help="print full command details before executing the command")

    subparser = parser.add_subparsers(required='True')

    # register command moduls und argparser arguments
    for mod in _CMD_MODULS:
        cmd_parser = mod.register(subparser)
        cmd_parser.set_defaults(func=mod.execute)

    return parser

def main() -> Ret:
    """ The program entry point function.

    Returns:
        int: System exit status.
    """
    ret_status = Ret.RET_OK

    # get parser
    parser = add_parser()
    printer = Printer()
    args = parser.parse_args()

    # In verbose mode print all program arguments
    if args.verbose:

        printer.set_verbose()

        print("Program arguments: ")

        for arg in vars(args):
            print(f"* {arg} = {vars(args)[arg]}")
        print("\n")

    # call command function and return exit status
    ret_status = args.func(args)

    if ret_status != Ret.RET_OK:
        printer.print_error(PrintType.ERROR, ret_status)

    return ret_status

################################################################################
# Main
################################################################################

if __name__ == "__main__":
    sys.exit(main())
