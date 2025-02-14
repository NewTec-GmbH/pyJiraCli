"""
Tests for the pyJiraCli help messages.
"""

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

from pyJiraCli.ret import Ret
from tests.conftest import Helpers

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################


def test_help(helpers: Helpers):
    """
    Test the help argument of the pyJiraCli and all its commands.
    """

    # No arguments should return the help message but fail as a required arg is missing.
    ret = helpers.run_pyjiracli([])
    assert Ret.CODE.RET_ERROR_ARGPARSE == ret.returncode  # Expect error.

    # Test the help option of the pyJiraCli.
    ret = helpers.run_pyjiracli(["--help"])
    assert Ret.CODE.RET_OK == ret.returncode  # Expect success.

    # Test the help flag of the pyJiraCli.
    ret = helpers.run_pyjiracli(["-h"])
    assert Ret.CODE.RET_OK == ret.returncode  # Expect success.

    # Get all commands of the pyJiraCli using the previous help command.
    help_message = ret.stdout.decode("utf-8")
    start_index = help_message.find("{")
    end_index = help_message.find("}")
    assert start_index != -1, help_message  # Start of command list not found.
    assert end_index != -1, help_message  # End of command list not found.

    # Extract the command list.
    command_list = help_message[start_index+1:end_index].split(",")

    # Test the help argument of all commands.
    for command in command_list:

        # Test the help option of the command.
        _test_help_option(helpers, command)

        # Test the help flag of the command.
        _test_help_flag(helpers, command)

        # Test the print command with no arguments.
        _test_command_without_arguments(helpers, command)


def _test_help_option(helpers: Helpers, command: str) -> None:
    """ Test the help option of the command."""

    ret = helpers.run_pyjiracli([command, "--help"])
    stdout = ret.stdout.decode("utf-8")

    # Expect OK.
    assert Ret.CODE.RET_OK == ret.returncode
    # Print usage message.
    assert f"usage: pyJiraCli {command} [-h]" in stdout


def _test_help_flag(helpers: Helpers, command: str) -> None:
    """ Test the help flag of the command."""

    ret = helpers.run_pyjiracli([command, "-h"])
    stdout = ret.stdout.decode("utf-8")

    # Expect OK.
    assert Ret.CODE.RET_OK == ret.returncode
    # Print usage message.
    assert f"usage: pyJiraCli {command} [-h]" in stdout


def _test_command_without_arguments(helpers: Helpers, command: str) -> None:
    """ Test the command without arguments."""

    ret = helpers.run_pyjiracli([command])
    stderr = ret.stderr.decode("utf-8")

    # Expect invalid arguments.
    assert Ret.CODE.RET_ERROR_ARGPARSE == ret.returncode
    # Print usage message.
    assert f"usage: pyJiraCli {command} [-h]" in stderr
    # Print error message.
    assert "error: the following arguments are required:" in stderr


################################################################################
# Main
################################################################################
