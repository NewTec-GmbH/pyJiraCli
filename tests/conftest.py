"""
This file contains fixtures that are used by all tests in the tests folder.
"""

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

import os
import subprocess
import pytest

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################


class Helpers:  # pylint: disable=too-few-public-methods
    """
    Helper class for common fixtures.
    """

    PROFILE_COMMAND = "profile"
    CI_PROFILE_NAME = "ci_profile"
    CI_JIRA_SERVER_URL = "http://localhost:2990/jira"
    CI_JIRA_USER_TOKEN = os.environ.get("CI_JIRA_USER_TOKEN", "DummyToken")

    @staticmethod
    def run_pyjiracli(arguments) -> subprocess.CompletedProcess:
        """
        Wrapper to run pyJiraCli command line.

        Args:
            arguments (list): List of arguments to pass to pyJiraCli.

        Returns:
            subprocess.CompletedProcess[bytes]: The result of the command. 
            Includes return code, stdout and stderr.
        """
        args = ["pyJiraCli"]  # The executable to run.
        args.extend(arguments)  # Add the arguments to the command.

        return subprocess.run(args,
                              # Capture stdout and stderr.
                              capture_output=True,
                              # Do not raise exception on non-zero exit code.
                              check=False,
                              # Do not run command in shell. Otherwise, it will not work on Linux.
                              shell=False)

    @staticmethod
    def create_profile() -> subprocess.CompletedProcess:
        """
        Create a profile for testing.
        Found in this class for easier reuse between commands.

        Returns:
            subprocess.CompletedProcess[bytes]: The result of the command. 
            Includes return code, stdout and stderr.
        """
        return Helpers.run_pyjiracli([Helpers.PROFILE_COMMAND, "add",
                                      "--server", Helpers.CI_JIRA_SERVER_URL,
                                      "--token", Helpers.CI_JIRA_USER_TOKEN,
                                      Helpers.CI_PROFILE_NAME])

    @staticmethod
    def remove_profile() -> subprocess.CompletedProcess:
        """
        Remove a profile for testing.
        Found in this class for easier reuse between commands.

        Returns:
            subprocess.CompletedProcess[bytes]: The result of the command. 
            Includes return code, stdout and stderr.
        """
        return Helpers.run_pyjiracli([Helpers.PROFILE_COMMAND, "remove", Helpers.CI_PROFILE_NAME])

################################################################################
# Functions
################################################################################


@pytest.fixture
def helpers() -> Helpers:
    """ Get helper class. """
    return Helpers

################################################################################
# Main
################################################################################
