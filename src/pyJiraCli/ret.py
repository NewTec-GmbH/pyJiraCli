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
from dataclasses import dataclass

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################


@dataclass
class Ret():
    """The Error codes of pyJiraCli tool."""

    class CODE(IntEnum):
        """ The exit statuses of the modules."""
        RET_OK                           = 0
        RET_ERROR                        = 1
        RET_ERROR_ARGPARSE               = 2 # Must be 2 to match the argparse error code.
        RET_ERROR_FILEPATH_INVALID       = 3
        RET_ERROR_WORNG_FILE_FORMAT      = 4
        RET_ERROR_ISSUE_NOT_FOUND        = 5
        RET_ERROR_FILE_OPEN_FAILED       = 6
        RET_ERROR_NO_USERINFORMATION     = 7
        RET_ERROR_PROFILE_NOT_FOUND      = 8
        RET_ERROR_NO_SERVER_URL          = 9
        RET_ERROR_CREATING_TICKET_FAILED = 10
        RET_ERROR_INVALID_SEARCH         = 11
        RET_ERROR_INVALID_URL            = 12
        RET_ERROR_JIRA_LOGIN             = 13

    MSG = {
        CODE.RET_OK:                           "Process successful.",
        CODE.RET_ERROR:                        "Error occurred.",
        CODE.RET_ERROR_ARGPARSE:               "Error while parsing arguments.",
        CODE.RET_ERROR_FILEPATH_INVALID:       "The provided filepath does not exist.",
        CODE.RET_ERROR_WORNG_FILE_FORMAT:      "Wrong file format for save file provided.",
        CODE.RET_ERROR_ISSUE_NOT_FOUND:        "Jira issue not found.",
        CODE.RET_ERROR_FILE_OPEN_FAILED:       "Failed to open file.",
        CODE.RET_ERROR_NO_USERINFORMATION:     "No user information was provided \
                                                or stored information file.",
        CODE.RET_ERROR_PROFILE_NOT_FOUND:      "The server profile does not exist.",
        CODE.RET_ERROR_NO_SERVER_URL:          "To add a new profile, the server url must \
                                                be provided with the --url option",
        CODE.RET_ERROR_CREATING_TICKET_FAILED: "creating the ticket on the jira server failed",
        CODE.RET_ERROR_INVALID_SEARCH:         "search string returned a jira error",
        CODE.RET_ERROR_INVALID_URL:            "The provided server url is invalid",
        CODE.RET_ERROR_JIRA_LOGIN:             "Login to jira server was not possible",
    }


@dataclass
class Warnings():
    """ The messages corresponding to the return values and warnings."""

    class CODE(IntEnum):
        """ Th Warnings of the modules."""
        WARNING_UNSAVE_CONNECTION      = 0
        WARNING_UNKNOWN_FILE_EXTENSION = 1
        WARNING_TOKEN_RECOMMENDED      = 2

    MSG = {
        CODE.WARNING_UNSAVE_CONNECTION:      "No certificate for server authentication found." + \
                                             " It's strongly advised, to add a certificate for " + \
                                             "your server profile.",
        CODE.WARNING_UNKNOWN_FILE_EXTENSION: "The provided file has an unknown file format. " + \
                                             "A new file with the same name and " + \
                                             "JSON file will be created.",
        CODE.WARNING_TOKEN_RECOMMENDED:      "No api token was found in this server profile. " + \
                                             "Its recommended to add a token to your server " +\
                                             "profile."
    }

################################################################################
# Functions
################################################################################
