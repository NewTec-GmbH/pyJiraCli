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

from pyJiraCli import cmd_import
from pyJiraCli import cmd_export
from pyJiraCli import cmd_search
from pyJiraCli import cmd_login
from pyJiraCli import cmd_print
from pyJiraCli.retval import Ret, prerr

from pyJiraCli.version import __version__, __author__, __email__, __repository__, __license__
################################################################################
# Variables5
################################################################################

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################
def add_parser():
    """"add parser for command line arguments"""

    parser = argparse.ArgumentParser(description="Program to handle JSON files.")
    parser.add_argument(
            "--version",
            action="version",
            version="%(prog)s " + __version__)

    subparser = parser.add_subparsers()

    cmd_import.add_parser(subparser)
    cmd_export.add_parser(subparser)
    cmd_search.add_parser(subparser)
    cmd_login.add_parser(subparser)
    cmd_print.add_parser(subparser)

    return parser.parse_args()

######################################################

######################################################
######################################################
def main():
    """The program entry point function.

    
    Returns:
        int: System exit status
    """
    # get parser arguments
    args = add_parser()

    # call command function and return exit status
    ret_status = args.func(args)

    if ret_status != Ret.RET_OK:
        prerr(ret_status)

    return ret_status
######################################################

################################################################################
# Main
################################################################################

if __name__ == "__main__":
    sys.exit(main())
