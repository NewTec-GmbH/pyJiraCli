"""
Attempts to create a test user, as the empty JIRA instance isn't provisioned with one.
Script derived from pycontribs/jira
https://github.com/pycontribs/jira/blob/eb0ec90e08ae24823e266b0128b852022d212982/make_local_jira_user.py
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
import time
import requests
from jira import JIRA

################################################################################
# Variables
################################################################################

CI_JIRA_URL = "http://localhost:2990/jira"
CI_JIRA_ADMIN = "admin"
CI_JIRA_ADMIN_PASSWORD = "admin"
CI_JIRA_USER = "jira_user"
CI_JIRA_USER_FULL_NAME = "Newly Created CI User"
CI_JIRA_USER_PASSWORD = "jira"
CI_JIRA_TEST_PROJECT = "TESTPROJ"

################################################################################
# Classes
################################################################################


def add_user_to_jira() -> None:
    """Add a user to Jira Server for CI testing purposes."""

    try:
        JIRA(
            CI_JIRA_URL,
            basic_auth=(CI_JIRA_ADMIN, CI_JIRA_ADMIN_PASSWORD),
        ).add_user(
            username=CI_JIRA_USER,
            email="user@example.com",
            fullname=CI_JIRA_USER_FULL_NAME,
            password=CI_JIRA_USER_PASSWORD,
        )

        print("user", CI_JIRA_USER)

    except Exception as e:  # pylint: disable=broad-except
        if "username already exists" not in str(e):
            raise e

    # pylint: disable=missing-timeout
    response = requests.post(CI_JIRA_URL + "/rest/pat/latest/tokens",
                             auth=("jira_user", 'jira'),
                             json={"name": "tokenName",
                                   "expirationDuration": 90
                                   })

    if response.status_code != 201:
        print("Failed to create token with status code", response.status_code)
    else:
        token = response.json().get("rawToken")
        print("token", token)
        os.environ["CI_JIRA_USER_TOKEN"] = token

        # pylint: disable=W1514
        with open(os.environ['GITHUB_ENV'], 'a') as fh:
            print(f'{"CI_JIRA_USER_TOKEN"}={token}', file=fh)


def create_project() -> None:
    """Create a project in Jira Server for CI testing purposes."""

    try:
        project = JIRA(
            CI_JIRA_URL,
            basic_auth=(CI_JIRA_ADMIN, CI_JIRA_ADMIN_PASSWORD),
        ).create_project(CI_JIRA_TEST_PROJECT)

        if project is False:
            print("Failed to create project.")
        else:
            print("Test project", CI_JIRA_TEST_PROJECT)

    except Exception as e:  # pylint: disable=broad-except
        if "A project with that name already exists." not in str(e):
            raise e

################################################################################
# Functions
################################################################################


if __name__ == "__main__":

    start_time = time.time()
    TIMEOUT_MINS = 15

    print(
        "waiting for instance of jira to be running, to add a user for CI system:\n"
        f"timeout = {TIMEOUT_MINS} mins"
    )

    while True:
        try:
            # pylint: disable=missing-timeout
            requests.get(CI_JIRA_URL + "rest/api/2/permissions")
            print("JIRA IS REACHABLE")
            add_user_to_jira()
            create_project()
            break

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as ex:
            print(f"encountered {ex} while waiting for the JiraServer docker")
            time.sleep(20)

        if start_time + 60 * TIMEOUT_MINS < time.time():
            raise TimeoutError(
                f"Jira server wasn't reachable within timeout {TIMEOUT_MINS}"
            )


################################################################################
# Main
################################################################################
