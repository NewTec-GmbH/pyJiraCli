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
CRED = '\033[91m'
CEND = '\033[0m'

class Ret(IntEnum):
    """"exit statuses of the modules"""
    RET_OK                           = 0
    RET_ERROR                        = 1
    RET_ERROR_JIRA_LOGIN             = 2
    RET_ERROR_FILE_NOT_FOUND         = 3
    RET_ERROR_WORNG_FILE_FORMAT      = 4
    RET_ERROR_ISSUE_NOT_FOUND        = 5
    RET_ERROR_FILE_OPEN_FAILED       = 6
    RET_ERROR_NO_USERINFORMATION     = 7
    RET_ERROR_MISSING_UNSERINFO      = 8
    RET_ERROR_MISSING_LOGIN_INFO     = 9
    RET_ERROR_CREATING_TICKET_FAILED = 10
    RET_ERROR_INFO_FILE_EXPIRED      = 11


RETURN_MSG = {
    Ret.RET_OK                           : "Process succesful",
    Ret.RET_ERROR                        : "Error occured",
    Ret.RET_ERROR_JIRA_LOGIN             : "Login to jira server was not possible",
    Ret.RET_ERROR_FILE_NOT_FOUND         : "Folder or File doesn't exist",
    Ret.RET_ERROR_WORNG_FILE_FORMAT      : "Wrong file format for save file provided",
    Ret.RET_ERROR_ISSUE_NOT_FOUND        : "Jira Issue not found",
    Ret.RET_ERROR_FILE_OPEN_FAILED       : "opening File failed",
    Ret.RET_ERROR_NO_USERINFORMATION     : "no user information was provided via cli " + \
                                           "or stored information file",
    Ret.RET_ERROR_MISSING_UNSERINFO      : "both -user and -pw option must be provided " + \
                                           "to store useriformation",
    Ret.RET_ERROR_MISSING_LOGIN_INFO     : "At least one of the options must be provided: " + \
                                           "(-user, -pw), -server or -delete",
    Ret.RET_ERROR_CREATING_TICKET_FAILED : "creating the ticket on the jira server failed",
    Ret.RET_ERROR_INFO_FILE_EXPIRED      : "the stored information has expired"
}
################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################
def prerr(error):
    """print exit error
    
    Args:
        error (Ret):    the return code for which an error shall be printed
    """
    print(CRED, "Error: ", RETURN_MSG[error], CEND)
