"""
Tests for the import command.
Requires a Jira instance to be running.
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
from pyJiraCli.ret import Ret
from tests.conftest import Helpers

################################################################################
# Variables
################################################################################

PROFILE_COMMAND = "profile"
CI_JIRA_USER = "jira_user"
CI_JIRA_USER_PASSWORD = "jira"
CI_PROFILE_NAME = "ci_profile"
CI_JIRA_SERVER_URL = "http://localhost:2990/jira"
CI_JIRA_USER_TOKEN = os.environ["CI_JIRA_USER_TOKEN"]

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################


def test_add(helpers: Helpers):
    """ Test the --add option. """
    ret = helpers.run_pyjiracli([PROFILE_COMMAND, "--add",
                                 "--url", CI_JIRA_SERVER_URL,
                                 "--token", CI_JIRA_USER_TOKEN,
                                 CI_PROFILE_NAME])

    # Expect OK.
    assert Ret.CODE.RET_OK == ret.returncode


def test_remove(helpers: Helpers):
    """ Test the --remove option. """
    ret = helpers.run_pyjiracli([PROFILE_COMMAND, "--remove", CI_PROFILE_NAME])

    # Expect OK.
    assert Ret.CODE.RET_OK == ret.returncode

################################################################################
# Main
################################################################################
