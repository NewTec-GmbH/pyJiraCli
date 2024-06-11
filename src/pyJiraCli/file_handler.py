""" The file handler manages all file operations."""

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
import os
import ctypes

from pyJiraCli.ret import Ret
################################################################################
# Variables
################################################################################
FILE_ATTRIBUTE_HIDDEN = 0x02
################################################################################
# Classes
################################################################################
class FileHandler:
    """ The file handler class provides file operations
        like open, close , read and write.
    """
    def __init__(self):
        self._file = None
        self._ext  = None
        self._path = None
        self._parent_path = None
        self._content = None

    def set_filepath(self, path:str) -> Ret.CODE:
        """ Set the path for the file contained in this Instance.

        Args:
            path (str): Path to the file.
        
        Returns:
        Ret:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
        """
        ret_status = Ret.CODE.RET_OK

        path_comps = path.split('/')

        if len(path_comps) == 1:
            path_comps = path.split('\\')

        if len(path_comps) == 1:
            path_comps = [*os.path.split(os.getcwd()), path_comps[0]]

        if path_comps[0] == '.':
            root_path_comps = os.path.split(os.getcwd())
            path_comps = [*root_path_comps, *path_comps[1:]]

        # remove eventual empty path components
        if '' in path_comps:
            path_comps.remove('')

        if path_comps[0][-1] == ':':
            # check if the first component is a drive name
            path_comps[0] += '\\'

        formatted_path = os.path.join(*path_comps)
        parent_path = os.path.join(*path_comps[:-1])

        if os.path.exists(formatted_path) or \
           os.path.exists(parent_path):
            self._ext = os.path.splitext(formatted_path)[-1]
            self._path = formatted_path
            self._parent_path = parent_path

            if os.path.isdir(formatted_path):
                self._ext = None
                self._path = formatted_path
                self._parent_path = formatted_path

        else:
            ret_status = Ret.CODE.RET_ERROR_FILEPATH_INVALID

        return  ret_status

    def read_file(self) -> Ret.CODE:
        """ Open the file in read mode and read its content
            to the file instance.

        Returns:
            Ret.CODE:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
        """
        ret_status = Ret.CODE.RET_OK

        if self._file is None:
            # open file in read mode
            ret_status = self.open_file(file_mode='r')

        if ret_status == Ret.CODE.RET_OK:
            self._content = self._file.read()

        self.close_file()

        return ret_status

    def get_file(self) -> object:
        """ Return the file object in 
            this instance.

        Returns:
            obj: The file object.
        """
        return self._file

    def get_file_extension(self) -> str:
        """ Return the file extension 
            of the file as a string.

        Returns:
            str: The file extension.
        """
        return self._ext

    def get_path(self) -> str:
        """ Return the path as a string.

        Returns:
            str: The existing filepath or parent folder path.
        """
        return self._path

    def get_parent_path(self) -> str:
        """ Return the parent path as a string.

        Returns:
            str: The existing parent folder path.
        """
        return self._parent_path

    def get_file_content(self) -> str:
        """ Return the file content
            of the file as string.

        Returns:
            str: The file content.
        """
        return self._content

    def write_file(self, file_input:str) -> Ret.CODE:
        """ Open the file in write mode
            and write the function argument
            to the file.

        Args:
            file_input (str): A string that'll be written to the file.

        Returns:
            Ret.CODE:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
        """
        ret_status = Ret.CODE.RET_OK

        if self._file is None:
            # open file in write mode
            ret_status = self.open_file(file_mode='w')

        if ret_status == Ret.CODE.RET_OK:
            self._file.write(file_input)

        self.close_file()

        return  ret_status

    def open_file(self, file_mode:str) -> Ret.CODE:
        """ Open the filepath in this instance
            and save the file obj.

        Args:
            file_mode (str): For reading files 'r' or for writing files 'w'.    

        Returns:
            Ret.CODE:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
        """
        ret_status = Ret.CODE.RET_OK

        try:
            self._file = open(self._path, mode=file_mode, encoding='utf-8') # pylint: disable=consider-using-with

        except (OSError, FileNotFoundError, IOError) as e:
            # print exception
            print(str(e))
            ret_status = Ret.CODE.RET_ERROR_FILE_OPEN_FAILED

        return  ret_status

    def hide_file(self) -> None:
        """ Set the file attribute "file hidden".
        """
        if self._path is not None:
            if os.path.exists(self._path):
                ctypes.windll.kernel32.SetFileAttributesW(self._path,
                                                      FILE_ATTRIBUTE_HIDDEN)

    def close_file(self) -> None:
        """ Close the file in the class instance.        
        """
        if self._file is not None:
            if not self._file.closed:
                self._file.close()

            self._file = None

    def delete_file(self) -> None:
        """ Delete the file stored in the
            class instance.
        """
        if self._file is not None:
            if not self._file.closed:
                self._file.close()
                self._file = None
                self._ext = None

        if os.path.exists(self._path):
            os.remove(self._path)

################################################################################
# Functions
################################################################################
