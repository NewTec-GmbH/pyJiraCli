"""
Tests for the search command.
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
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USEd
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

################################################################################
# Imports
################################################################################

import json
from pyJiraCli.ret import Ret
from tests.conftest import Helpers

################################################################################
# Variables
################################################################################

PROJ_KEY = "TESTPROJ"
OUTPUT_FILE_NAME = "export.json"

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################


def test_search(helpers: Helpers):
    """ Test the search command. """
    credentials = ["--server", helpers.CI_JIRA_SERVER_URL,
                   "--token", helpers.CI_JIRA_USER_TOKEN]
    max_number_of_issues = 1
    jql_string = f"project = {PROJ_KEY}"

    ret = helpers.run_pyjiracli(
        credentials + ["search",
                       "--max", str(max_number_of_issues),
                       jql_string])

    # Expect OK.
    assert Ret.CODE.RET_OK == ret.returncode

    # Test export to file.
    max_number_of_issues = 3
    ret = helpers.run_pyjiracli(
        credentials + ["search",
                       "--max", str(max_number_of_issues),
                       "--file", OUTPUT_FILE_NAME,
                       jql_string])

    # Expect OK.
    assert Ret.CODE.RET_OK == ret.returncode

    # Check the exported file.
    with open(OUTPUT_FILE_NAME, "r", encoding="UTF-8") as file:
        exported = json.load(file)

    assert exported["search"] == jql_string
    assert exported["max"] == max_number_of_issues
    assert exported["found"] == max_number_of_issues
    assert len(exported["issues"]) == max_number_of_issues


################################################################################
# Main
################################################################################
