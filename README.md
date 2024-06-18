# pyJiraCli <!-- omit in toc -->

pyJiraCli is a command-line tool designed for handling Jira tickets efficiently. With pyJiraCli, you can import/export tickets to JSON files, create tickets on the server using JSON files and search for tickets based on a search string.

[![License](https://img.shields.io/badge/license-bsd-3.svg)](https://choosealicense.com/licenses/bsd-3-clause/)
[![Repo Status](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![CI](https://github.com/NewTec-GmbH/pyJiraCli/actions/workflows/ci.yml/badge.svg)](https://github.com/NewTec-GmbH/pyJiraCli/actions/workflows/ci.yml)

* [Installation](#installation)
* [Overview](#overview)
* [Usage](#usage)
* [Commands](#commands)
  * [Export](#export)
  * [Import](#import)
  * [Search](#search)
  * [Print](#print)
  * [Profile](#profile)
  * [Get_Sprints](#get_sprints)
* [Add a command](#add-a-command)
* [Examples](#examples)
  * [JSON example file](#json-example-file)
* [Used Libraries](#used-libraries)
* [Issues, Ideas And Bugs](#issues-ideas-and-bugs)
* [License](#license)
* [Contribution](#contribution)

## Installation

```cmd
git clone https://github.com/NewTec-GmbH/pyJiraCli.git
cd pyJiraCli
pip install .
```

## Overview

![overview](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/NewTec-GmbH/pyJiraCli/main/design/context.puml)

## Usage

Show help information:

```cmd
pyJiraCli --help
```

Output:

```cmd
usage: pyJiraCli [-h] [--profile <profile>] [-u <user>] [-p <password>] [-t <token>] [-s <server URL>] [--version] [-v] {export,import,search,print,profile,get_sprints} ...

A CLI tool to import and export Jira issues between server and JSON files.

positional arguments:
  {export,import,search,print,profile,get_sprints}
    export              Export a ticket from a Jira Server to a JSON file.
    import              Import a Jira Issue from a JSON file.
    search              Search for the Jira server for issues using the specified filter string.
    print               Print the Jira Issue details to the console.
    profile             Add, update or delete server profiles.
    get_sprints         Get all sprints in a board and save the sprint data into a JSON file.

options:
  -h, --help            show this help message and exit
  --profile <profile>   The name of the server profile which shall be used for this process
  -u <user>, --user <user>
                        The user to authenticate with the Jira server
  -p <password>, --password <password>
                        The password to authenticate with the Jira server
  -t <token>, --token <token>
                        The token to authenticate with the Jira server
  -s <server URL>, --server <server URL>
                        The Jira server URL to connect to.
  --version             show program's version number and exit
  -v, --verbose         Print full command details before executing the command. Enables logs of type INFO and WARNING.

Copyright (c) 2024 NewTec GmbH - BSD 3-Clause - Find the project on GitHub: documentation, https://github.com/NewTec-GmbH/pyJiraCli
```

## Commands

All added command modules must provide an "execute()" and a "register()" function.

### Export

Export a ticket from a Jira Server to a JSON file

```cmd
pyJiraCli export --help
```

Output:

```cmd
usage: pyJiraCli export [-h] [--file <path to file>] issue

positional arguments:
  issue                 Jira issue key

options:
  -h, --help            show this help message and exit
  --file <path to file>
                        Absolute file path or filepath relative to the current working directory. 
                        The file format must be JSON.
                        If a different file format is provided, the file extension will be replaced. 
```

Example:

```cmd
pyJiraCli export ISSUE-2291 --path issues --filename important_issue
```

This creates the file `./issues/important_issue.json`.

### Import

Import a ticket from a JSON file.
Creates a Jira issue on the server with the ticket data specified in the file.

```cmd
pyJiraCli import --help
```

Output:

```cmd
usage: pyJiraCli import [-h] file

positional arguments:
  file        Path to the input file.

options:
  -h, --help  show this help message and exit
```

Example:

```cmd
pyJiraCli import important_issue.json
```

This creates an issue on the Jira server using the data specified in `important_issue.json`.

More examples can be found in [the examples folder](./examples/import_issues/README.md).

### Search

Search the Jira server for issues using the specified filter string. The string must be in JQL (Jira Query Language) format.

If you need help working with filters, check out <https://confluence.atlassian.com/jirasoftwareserver/advanced-searching-939938733.html>.
Also, the results can be ordered by command, just add "order by" to your cmd

```cmd
pyJiraCli search --help
```

Output:

```cmd
usage: pyJiraCli search [-h] [--max <MAX>] [--save <PATH TO FILE>] filter

positional arguments:
  filter                Filter string to search for. Must be in JQL format.

options:
  -h, --help            show this help message and exit
  --max <MAX>           Maximum number of issues that may be found.Default is 50.If set to 0, all issues will be searched.
  --save <PATH TO FILE> Absolute filepath or filepath relative to the current work directory to a JSON file.
```

Example:

```cmd
pyJiraCli search --max 50 "project=PROJ order by created desc"
```

This will find the 50 latest issues in project PROJ and display them by descending creation date.

More examples can be found in [the examples folder](./examples/search/README.md).

### Print

Print the Jira Issue details to the console.

```cmd
pyJiraCli print --help
```

Output:

```cmd
usage: pyJiraCli print [-h] issueKey

positional arguments:
  issueKey    The Jira Issue Key of the Issue to print.

options:
  -h, --help  show this help message and exit
```

Example:

```cmd
pyJiraCli print ISSUE-2291
```

The output depends on the fields configured by the Jira server.

### Profile

Add, delete or update server profiles.

The profile contains following data:

* name: A unique profile name by which you can reference your profile. (required)
* server: The server url where your jira server is located. (required)
* token: An api token to allow for faster access. (optional)
* certificate: A server certificate for your company/jira instance. (optional)

When adding a profile, the server url and token are required.
The certificate is optional and can also be added later on,
with the --update option.
Username and password are not valid to create a profile for security reasons.

```cmd
pyJiraCli profile --help
```

Output:

```cmd
usage: pyJiraCli profile [-h] [--cert <certificate path>] (--add | --remove | --update) <profile name>

options:
  -h, --help            show this help message and exit

Profile Data:
  <profile name>        The Name under which the profile will be saved.
  --cert <certificate path>
                        The server SSL certificate.

profile operations:
  Only one operation type can be processed at a time.

  --add, -a             Add a new server profile.
  --remove, -r          Delete an existing server profile.
  --update, -u          Update an existing server profile with new data.
```

Example:

```cmd
pyJiraCli --server https://my-jira-instance.com --token This-Is-an-Example-Token profile --add new_profile --cert C:\\Path\\To\\Certificate.crt 
```

This will create a new profile with the name "new_profile" and saves all possible profile information.

### Get_Sprints

Analog to the export command for issue, you can get raw Sprint data for boards. \
The board name needs to fit the name on the jira server. \
You can choose where to store the data with the --file option.

```cmd
pyJiraCli get_sprints --help
```

Output:

```cmd
usage: pyJiraCli get_sprints [-h] [--file <path to file>] board

positional arguments:
  board                 The board for which the sprints shall be stored.

options:
  -h, --help            show this help message and exit
  --file <path to file>
                        Absolute file path or filepath relativ to the current working directory. The file format must be JSON.
```

## Add a command

In order to add a new command to the program, the following steps must be taken:

1. A file for the command must be created: `src/cmd_<command_name>.py`

<details>
<summary>Code</summary>
<p>

```py
# import the exit codes
from pyJiraCli.retval import Ret

def register(subparser):
  ''' register the command and its options '''

    sub_parser_cmd = subparser.add_parser('cmd',
                                    help="a custom command")

    sub_parser_cmd.add_argument('postional arg',
                          type=str,
                          help="Some positional argument that is read as a string.")

    sub_parser_cmd.add_argument('--option',
                          type=str,
                          metavar='<username>',
                          help="Some option that is read as a string and stored in a metavar.")
    
    sub_parser_cmd.add_argument('--bool_option',
                          action="store_true",
                          help="store 'True'' in args.bool_option if the option \
                                is set on the commandline \
                                otherwise store 'False'")
    
    # make sure to return the command parser
    return sub_parser_cmd

def execute(args):
  ''' execute function, your module entry point will be here
      returns the module exit code: 
      retval.Ret.CODE.RET_OK'''
    ret_status = Ret.CODE.RET_OK

    ret_status = execute_cmd(args)

    return ret_status
```

</p>
</details>

2. Add the command to `src/__main__.py`.

<details>
<summary>Code</summary>
<p>

```py
################################################################################
# Imports
################################################################################
from pyJiraCli import cmd_import
from pyJiraCli import cmd_export
from pyJiraCli import cmd_search
from pyJiraCli import cmd_print
from pyJiraCli import cmd_profile
from pyJiraCli import cmd_get_sprints

from pyJiraCli import cmd_custom # import your module

################################################################################
# Variables
################################################################################

# Add command modules here
_CMD_MODULES = [
    cmd_export,
    cmd_import,
    cmd_search,
    cmd_print,
    cmd_profile,
    cmd_get_sprints
]
```

</p>
</details>

3. Import ```retval.py``` and add further error codes and messages if needed.

<details>
<summary>Code</summary>
<p>

```py
class Ret(IntEnum):
    """ The exit statuses of the modules."""
    RET_OK                           = 0
    RET_ERROR                        = 1
    RET_ERROR_JIRA_LOGIN             = 2
    RET_ERROR_FILEPATH_INVALID       = 3
    RET_ERROR_WORNG_FILE_FORMAT      = 4
    RET_ERROR_ISSUE_NOT_FOUND        = 5
    RET_ERROR_FILE_OPEN_FAILED       = 6
    RET_ERROR_NO_USERINFORMATION     = 7
    RET_ERROR_MISSING_UNSERINFO      = 8
    RET_ERROR_MISSING_LOGIN_DATA     = 9
    RET_ERROR_MISSING_SERVER_URL     = 10
    RET_ERROR_MISSING_DATATYPE       = 11
    RET_ERROR_CREATING_TICKET_FAILED = 12
    RET_ERROR_INVALID_SEARCH         = 13

class Warnings(IntEnum):
    """ Th Warnings of the modules."""
    WARNING_UNSAVE_CONNECTION      = 0
    WARNING_UNKNOWN_FILE_EXTENSION = 1
    WARNING_TOKEN_RECOMMENDED      = 2

```

</p>
</details>

## Examples

### JSON example file

  With version v1 the generated JSON files will have following format:

```ticket.json```

```json
{
    "issue_key" : "ISSUE-TEST-1043",
    "project" : "ISSUE-TEST",
    "duedate" : "08-23-2024",
    "assignee" : "somebody else",
}
```

  In further versions this might change with the possibility for the user to provide file templates on how JSON files shall be read and written

## Used Libraries

Used 3rd party libraries which are not part of the standard Python package:

* [jira](https://pypi.org/project/jira/) - Python library for interacting with JIRA via REST APIs - BSD License (BSD-2-Clause).
* [colorama](https://github.com/tartley/colorama) - ANSI color support - BSD-3 License
* [cryptography](https://pypi.org/project/cryptography/) - cryptography is a package which provides cryptographic recipes and primitives to Python developers. - Apache Software License, BSD License (Apache-2.0 OR BSD-3-Clause)
* [toml](https://github.com/uiri/toml) - Parsing [TOML](https://en.wikipedia.org/wiki/TOML) - MIT License

## Issues, Ideas And Bugs

If you have further ideas or you found some bugs, great! Create a [issue](https://github.com/NewTec-GmbH/pyJiraCli/issues) or if you are able and willing to fix it by yourself, clone the repository and create a pull request.

## License

The whole source code is published under [BSD-3-Clause](https://github.com/NewTec-GmbH/pyJiraCli/blob/main/LICENSE).
Consider the different licenses of the used third party libraries too!

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, shall be licensed as above, without any additional terms or conditions.
