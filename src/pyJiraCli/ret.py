"""The Error codes of pyJiraCli tool."""
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
from enum import IntEnum
################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################
class Ret(IntEnum):
    """ The exit statuses of the modules."""
    RET_OK                           = 0
    RET_ERROR                        = 1
    RET_ERROR_JIRA_LOGIN             = 2
    RET_ERROR_FILEPATH_INVALID       = 3
    RET_ERROR_WORNG_FILE_FORMAT      = 4
    RET_ERROR_ISSUE_NOT_FOUND        = 5
    RET_ERROR_FILE_OPEN_FAILED       = 6
    RET_ERROR_NO_USERINFORMATION     = 7
    RET_ERROR_MISSING_UNSERINFO      = 8
    RET_ERROR_MISSING_LOGIN_DATA     = 9
    RET_ERROR_MISSING_DATATYPE       = 10
    RET_ERROR_CREATING_TICKET_FAILED = 11
    RET_ERROR_INVALID_SEARCH         = 12

class Warnings(IntEnum):
    """ Th Warnings of the modules."""
    WARNING_UNSAVE_CONNECTION      = 0
    WARNING_SERVER_URL_MISSING     = 1
    WARNING_CSV_OPTION_WRONG       = 2
    WARNING_UNKNOWN_FILE_EXTENSION = 3
    WARNING_INFO_FILE_EXPIRED      = 4
################################################################################
# Functions
################################################################################
