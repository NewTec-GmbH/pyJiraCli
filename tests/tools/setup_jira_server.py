"""
Attempts to create a test user, as the empty JIRA instance isn't provisioned with one.
Script derived from pycontribs/jira
https://github.com/pycontribs/jira/blob/eb0ec90e08ae24823e266b0128b852022d212982/make_local_jira_user.py
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
CI_FILTER_NAME = "CI_FILTER"
CI_FILTER_DESCRIPTION = "CI_FILTER_DESCRIPTION"
CI_FILTER_JQL = "type = Bug and resolution is empty"
CI_BOARD_NAME = "CI_BOARD"
CI_SPRINT_NAME = "CI_SPRINT"

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################


def _add_user_to_jira(jira: JIRA) -> str:
    """Add a user to Jira Server for CI testing purposes."""
    created_user_key = ""

    try:
        # Create user.
        jira.add_user(
            username=CI_JIRA_USER,
            email="user@example.com",
            fullname=CI_JIRA_USER_FULL_NAME,
            password=CI_JIRA_USER_PASSWORD,
            ignore_existing=True
        )

        user_list = jira.search_users(user=CI_JIRA_USER)
        created_user = user_list[0]

        created_user_key = created_user.key
        print("user", created_user.name)
        print("user key", created_user_key)

    except Exception as e:  # pylint: disable=broad-except
        if "username already exists" not in str(e):
            raise e

    # Create token for user.
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

        try:

            # Save token to GitHub environment.
            # pylint: disable=W1514
            with open(os.environ['GITHUB_ENV'], 'a') as fh:
                print(f'{"CI_JIRA_USER_TOKEN"}={token}', file=fh)
        except Exception:  # pylint: disable=broad-except
            # GITHUB_ENV only exists in the CI.
            pass

    return created_user_key


def _create_project(jira: JIRA) -> None:
    """Create a project in Jira Server for CI testing purposes."""

    try:
        project = jira.create_project(CI_JIRA_TEST_PROJECT)

        if project is False:
            print("Failed to create project.")
        else:
            print("Test project", CI_JIRA_TEST_PROJECT)
            issue_types = jira.project_issue_types(CI_JIRA_TEST_PROJECT)
            print("Issue types", issue_types)

    except Exception as e:  # pylint: disable=broad-except
        if "A project with that name already exists." not in str(e):
            raise e


def _create_cert() -> None:
    """Create a certificate for Jira Server for CI testing purposes."""

    with open("cert.pem", "w", encoding="UTF-8") as cert_file:
        cert_file.write("HELLO WORLD")
        print("cert.pem created.")


def _create_sprint(jira: JIRA, created_user_key: str) -> None:
    """Create a sprint for Jira Server for CI testing purposes."""
    jira_filter = jira.create_filter(
        CI_FILTER_NAME, CI_FILTER_DESCRIPTION, CI_FILTER_JQL)

    if jira_filter is None:
        print("Failed to create filter.")
        return

    board = jira.create_board(CI_BOARD_NAME, jira_filter.id)

    if board is None:
        print("Failed to create board.")
        return

    sprint = jira.create_sprint(CI_SPRINT_NAME, board.id)

    if sprint is None:
        print("Failed to create sprint.")
        return

    print(f"Board {CI_BOARD_NAME} with sprint {jira_filter.id} created.")

    # pylint: disable=missing-timeout
    response = requests.post(CI_JIRA_URL + f"/rest/api/2/filter/{jira_filter.id}/permission",
                             auth=(CI_JIRA_ADMIN, CI_JIRA_ADMIN_PASSWORD),
                             json={
                                 "type": "user",
                                 "userKey": created_user_key,
                                 "view": True,
                                 "edit": True
                             })

    if response.status_code != 201:
        print("Failed to create filter shares with response code",
              response.status_code)
        print(response.json())
        print(response.request)
    else:
        print("Filter shares created.")


def _setup_server() -> None:
    """Setup Jira Server for CI testing purposes."""

    jira = JIRA(
        CI_JIRA_URL,
        basic_auth=(CI_JIRA_ADMIN, CI_JIRA_ADMIN_PASSWORD),
    )

    created_user_key = _add_user_to_jira(jira)
    _create_project(jira)
    _create_cert()
    _create_sprint(jira, created_user_key)


################################################################################
# Main
################################################################################


if __name__ == "__main__":

    start_time = time.time()
    TIMEOUT_MINS = 20

    print(
        "waiting for instance of jira to be running, to add a user for CI system:\n"
        f"timeout = {TIMEOUT_MINS} mins"
    )

    while True:
        try:
            # pylint: disable=missing-timeout
            requests.get(CI_JIRA_URL + "rest/api/2/permissions")
            print("JIRA IS REACHABLE")
            _setup_server()
            break

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as ex:
            print(f"encountered {ex} while waiting for the JiraServer docker")
            time.sleep(60)

        if start_time + 60 * TIMEOUT_MINS < time.time():
            raise TimeoutError(
                f"Jira server wasn't reachable within timeout {TIMEOUT_MINS}"
            )
