"""
Tests for the import and export commands.
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

ISSUE_KEY = "TESTPROJ-1"
OUTPUT_FILE_NAME = "export.json"

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################


def test_import_export(helpers: Helpers):
    """ Test the import and export commands. """
    credentials = ["--server", helpers.CI_JIRA_SERVER_URL,
                   "--token", helpers.CI_JIRA_USER_TOKEN]

    # Import a single issue.
    ret = helpers.run_pyjiracli(
        ["import"] + credentials + ["./examples/import_issues/single_issue.json"])
    assert Ret.CODE.RET_OK == ret.returncode

    # Import multiple issues.
    ret = helpers.run_pyjiracli(
        ["import"] + credentials + ["./examples/import_issues/multiple_issues.json"])
    assert Ret.CODE.RET_OK == ret.returncode

    # Import sub-issues.
    ret = helpers.run_pyjiracli(
        ["import"] + credentials + ["./examples/import_issues/sub_issues.json"])
    assert Ret.CODE.RET_OK == ret.returncode

    # Export the single issue.
    ret = helpers.run_pyjiracli(
        ["export"] + credentials + ["--file", OUTPUT_FILE_NAME, ISSUE_KEY])

    assert Ret.CODE.RET_OK == ret.returncode

    # Compare the exported file with the original.
    with open("examples/import_issues/single_issue.json", "r", encoding="UTF-8") as file:
        original = json.load(file)

    with open(OUTPUT_FILE_NAME, "r", encoding="UTF-8") as file:
        exported = json.load(file)

    original_summary = original["issues"][0]["summary"]
    exported_summary = exported["fields"]["summary"]

    assert original_summary == exported_summary

################################################################################
# Main
################################################################################
