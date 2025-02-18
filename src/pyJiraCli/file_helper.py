""" The file helper provides common file utilities. """

# BSD 3-Clause License
#
# Copyright (c) 2025, NewTec GmbH
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

import os

from pyJiraCli.ret import Ret, Warnings
from pyJiraCli.printer import Printer as LOG


################################################################################
# Variables
################################################################################


################################################################################
# Classes
################################################################################

class FileHelper:
    """ The file helper class provides common file operations. """
    # pylint: disable=too-few-public-methods

    def __init__(self):
        pass

    @staticmethod
    def process_file_argument(default_name: str, file_arg: str) -> tuple[Ret.CODE, str]:
        """ Processes the file argument provided by the user and returns it corrected/checked.

        If file_arg is None, the method returns a default file path using default_name with
        a .json extension.
        If file_arg is provided, the method checks the file extension:
            If there is no extension, it appends .json to file_arg.
            If the extension is not .json, it logs a warning and changes the extension to .json.
            If the extension is .json, it returns file_arg as is.
            If none of the conditions are met, it returns an error code indicating
            an invalid file path.

        Args:
            default_name (str): The default name of the file.
            file_arg (str): The file argument provided by the user (optional).

        Returns:
            tuple[Ret.CODE, str]: A tuple containing a return code (Ret.CODE) and the
            processed file path (str).
        """

        # If no file arg is provided, use the issue key as filename.
        if file_arg is None:
            return Ret.CODE.RET_OK, f"./{default_name}.json"

        # Check if the file extension of file_arg is correct; otherwise, correct it.

        first, ext = os.path.splitext(file_arg)

        if ext is None:
            return Ret.CODE.RET_OK, file_arg + '.json'

        if ext != '.json':
            LOG.print_info(Warnings.MSG.get(Warnings.CODE.WARNING_UNKNOWN_FILE_EXTENSION))
            return Ret.CODE.RET_OK, first + '.json'

        return Ret.CODE.RET_OK, file_arg

    @staticmethod
    # pylint: disable=R1732
    def open_file(file_path: str, mode: str) -> any:
        """ Opens a file (encoding="UTF-8") in the given mode.

        Args:
            file_path (str): The path to the file to open.
            mode (str): The mode to open the file in.

        Returns:
            file: The opened file.

        Raises:
            IOError: If the file does not exist.
            IOError: If the file cannot be accessed.
            IOError: If the file cannot be opened.
        """
        try:
            file = open(file_path, mode, encoding="UTF-8")
            return file

        except FileNotFoundError as exc:
            raise IOError(f"File '{file_path}' not found.") from exc
        except PermissionError as exc:
            raise IOError(f"Permission denied for '{file_path}'.") from exc
        except Exception as exc:
            raise IOError(f"Error opening file '{file_path}': {exc}") from exc
