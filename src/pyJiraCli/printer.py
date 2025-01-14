""" Contains the print error function and 
    the error messages corresponding to 
    the exit codes."""

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
from colorama import Fore, Style

from pyJiraCli.print_type import PrintType
from pyJiraCli.ret import Ret, Warnings

################################################################################
# Variables
################################################################################
COLOR = {
    PrintType.ERROR   : Fore.RED,
    PrintType.WARNING : Fore.YELLOW,
    PrintType.INFO    : Fore.WHITE
}

TYPE = {
    PrintType.ERROR   : "Error",
    PrintType.WARNING : "Warning",
    PrintType.INFO    : "Info"
}

INFO_TAB = "      "
################################################################################
# Classes
################################################################################
class Printer:
    """ The printer class.
        Prints errors, warnings and infos. 
        Infos and warnings are only printed,
        if verbose mode is set.
    """
    _print_verbose = False

    def __init__(self):
        pass

    @classmethod
    def set_verbose(cls):
        """Set verbose mode for all instances of the class."""
        cls._print_verbose = True

    def print_error(self, err_type: PrintType, error: Ret = Ret.CODE.RET_OK) -> None:
        """ Print the exit error.
    
        Args:
            type (PrintType)    The type of the msg (Error, Warning or Info).
            error (Ret):        The return code for which an error shall be printed.
        """
        if err_type is PrintType.WARNING and \
           self._print_verbose:
            print(COLOR[err_type] + TYPE[err_type] + ": " +
                  Style.RESET_ALL + Warnings.MSG[error])

        elif err_type is PrintType.ERROR:
            print(COLOR[err_type] + TYPE[err_type] + ": " +
                  Style.RESET_ALL + Ret.MSG[error])

    def print_info(self, *args:str) -> None:
        """ Print the information to the console.
    
        Args:
            args (*str):          The information that will be printed.
        """
        first_line = True

        if self._print_verbose:
            for arg in args:
                if first_line:
                    print("Info: " + arg)
                    first_line = False

                else:
                    print(INFO_TAB + arg)

################################################################################
# Functions
################################################################################
