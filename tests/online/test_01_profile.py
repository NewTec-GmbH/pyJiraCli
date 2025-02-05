"""
Tests for the profile command.
Requires a Jira instance to be running.
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

CERT_NAME = "cert.pem"

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################


def test_profile_operation(helpers: Helpers):
    """ Test the --add option. """
    # Remove any existing profile.
    ret = helpers.remove_profile()

    # Expect OK.
    assert Ret.CODE.RET_OK == ret.returncode

    # Create a new profile.
    ret = helpers.create_profile()

    # Expect OK.
    assert Ret.CODE.RET_OK == ret.returncode

    # Try to create the profile again.
    ret = helpers.create_profile()

    # Expect ERROR.
    assert Ret.CODE.RET_ERROR == ret.returncode

    # Remove the profile.
    ret = helpers.remove_profile()

    # Expect OK.
    assert Ret.CODE.RET_OK == ret.returncode

    # Try to create the profile again.
    ret = helpers.create_profile()

    # Expect OK.
    assert Ret.CODE.RET_OK == ret.returncode

    # Update the profile.
    ret = helpers.run_pyjiracli(
        [Helpers.PROFILE_COMMAND, "update", "--cert", CERT_NAME, Helpers.CI_PROFILE_NAME])

    # Expect OK.
    assert Ret.CODE.RET_OK == ret.returncode

################################################################################
# Main
################################################################################
