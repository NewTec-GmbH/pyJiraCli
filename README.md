# pyJiraCli <!-- omit in toc -->

pyJiraCli is a command-line tool designed for handling Jira tickets efficiently. With pyJiraCli, you can import/export tickets to JSON/CSV files, create tickets on the server using JSON/CSV files and search for tickets based on a search string.

[![License](https://img.shields.io/badge/license-bsd-3.svg)](https://choosealicense.com/licenses/bsd-3-clause/)
[![Repo Status](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![CI](https://github.com/NewTec-GmbH/pyJiraCli/actions/workflows/ci.yml/badge.svg)](https://github.com/NewTec-GmbH/pyJiraCli/actions/workflows/ci.yml)

* [Installation](#installation)
* [Overview](#overview)
* [Usage](#usage)
* [Commands](#commands)
  * [Delete](#delete)
  * [Export](#export)
  * [Import](#import)
  * [Login](#login)
  * [Search](#search)
  * [Print](#print)
* [Add a command](#add-a-command)
* [Examples](#examples)
  * [JSON example file](#json-example-file)
  * [CSV example file](#csv-example-file)
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
usage: pyJiraCli [-h] [--user <username>] [--password <password>] [--version] [--verbose] {export,import,search,login,delete,print} ...

A CLI tool to import and export Jira issues between server and JSON or CSV files.

positional arguments:
  {export,import,search,login,delete,print}
    export              export jira issue to json file
    import              Import a Jira Issue from a JSON or a CSV file.
    search              Search for the Jira server for issues using the specified filter string.
    login               Save the login information into an encrypted file for easier use.
    delete              delete login information
    print               Print the Jira Issue details to the console.

options:
  -h, --help            show this help message and exit
  --user <username>, -u <username>
                        Jira username, if not provided with login command.
  --password <password>, -p <password>
                        Jira password, if not provided with login command.
  --version, -v         show program's version number and exit
  --verbose             Print full command details before executing the command. Enables logs of type INFO and WARNING.

Copyright (c) 2024 NewTec GmbH - BSD 3-Clause - Find the project on GitHub: documentation, https://github.com/NewTec-GmbH/pyJiraCli
```

## Commands

All added command modules must provide an "execute()" and a "register()" function.

### Delete

Delete the saved login data. See [login](#login) for more details.

```cmd
pyJiraCli delete --help
```

Output:

```cmd
usage: pyJiraCli delete [-h] [--default] [--userinfo] [--server] [--token] [--cert]

options:
  -h, --help      show this help message and exit

data type to delete:
  --default, -d   Delete the server URL of the default server.
  --userinfo, -i  Delete the user information (username and password).
  --server, -s    Delete the server URL of the secondary server.
  --token, -t     Delete the API token for Jira server.
  --cert, -c      Delete the authentification certificate for Jira server.
```

Example:

```cmd
pyJiraCli delete -i 
```

This command deletes the saved user info.

### Export

Export a ticket from a Jira Server to a JSON or CSV file

```cmd
pyJiraCli export --help
```

Output:

```cmd
usage: pyJiraCli export [-h] [--path <folder_path>] [--filename <filename>] [--csv] issue

positional arguments:
  issue                 Jira issue key

options:
  -h, --help            show this help message and exit
  --path <folder_path>  Destination folder for the output file. Folder must exist.
  --filename <filename>
                        Name of the output file. Default is the issue key.
  --csv                 Save data in CSV file format.
```

Example:

```cmd
pyJiraCli export ISSUE-2291 --path issues --filename important_issue
```

This creates the file `./issues/important_issue.json`.

### Import

Import a ticket from a JSON or CSV file.
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

This creates an issue on the Jira server using the metadata specified in `important_issue.json`.

### Login

Save the login data to an encrypted file for easier use.

Following combinations are accepted:

* username and password.
* email and API token.

To store the email address use option --user.

Two server addresses can be stored, either as the default or a secondary server. The server cannot be set in the same command as the user credentials.

An expiration date can be set using the `--expiration` option, and its modifiers.

```cmd
pyJiraCli login --help
```

Output:

```cmd
usage: pyJiraCli login [-h] [--expiration <time>] [--min | --day | --month] (--default | --userinfo | --server | --token | --cert) <data1> [<data2>]

options:
  -h, --help           show this help message and exit
  --expiration <time>  Time after which the stored login info will expire. Default value = 60 days

data:
  <data1>              <username, token, url>
  <data2>              optional <password>

Expiration time options:
  Only one option can be used for setting the expiration time.

  --min                Expiration time in minutes.
  --day                Expiration time in days.
  --month              Expiration time in months.

Datatype options:
  Only one option can be used to specify the datatype.

  --default, -d        The server URL of the default server.
  --userinfo, -i       The user information (username and password).
  --server, -s         The server URL of the secondary server.
  --token, -t          The API token for Jira server.
  --cert, -c           The authentification certificate for Jira server.
```

Examples:

Set the default server URL

```cmd
pyJiraCli login --default https://my.jira.server/
```

Set the secondary server URL:

```cmd
pyJiraCli login --server https://my.other.jira.server/
```

Set your API token:

```cmd
pyJiraCli login --token <xxxxxxxxxxxxxxx> # 
```

### Search

Search the Jira server for issues using the specified filter string. The string must be in JQL (Jira Query Language) format.

If you need help working with filters, check out <https://confluence.atlassian.com/jirasoftwareserver/advanced-searching-939938733.html>.
Also, the results can be ordered by command, just add "order by" to your cmd

```cmd
pyJiraCli search --help
```

Output:

```cmd
usage: pyJiraCli search [-h] [--max <MAX>] filter

positional arguments:
  filter       Filter string to search for. Must be in JQL format.

options:
  -h, --help   show this help message and exit
  --max <MAX>  Maximum number of issues that may be found. Default is 50.
```

Example:

```cmd
pyJiraCli search --max 50 "project=PROJ order by created desc"
```

This will find the 50 latest issues in project PROJ and display them by descending creation date.

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

## Add a command

In order to add a new command to the programm, the following steps must be taken:

1. A file for the command must be created: `src/cmd_<command_name>.py`

<details>
<summary>Code</summary>
<p>

```py
# import the exit codes
from pyJiraCli.retval import Ret

def register(subparser):
  ''' register the command and its options '''

    sb_cmd = subparser.add_parser('cmd',
                                    help="a custom command")

    sb_cmd.add_argument('postional arg',
                          type=str,
                          help="Some positional argument that is read as a string.")

    sb_cmd.add_argument('--option',
                          type=str,
                          metavar='<username>',
                          help="Some option that is read as a string and stored in a metavar.")
    
    sb_cmd.add_argument('--bool_option',
                          action="store_true",
                          help="store 'True'' in args.bool_option if the option \
                                is set on the commandline \
                                otehrwise store 'False'")
    
    # make sure to return the command parser
    return sb_cmd

def execute(args):
  ''' execute function, your module enty point will be here
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
from pyJiraCli import cmd_login
from pyJiraCli import cmd_print

from pyJiraCli import cmd_custom # import your module

################################################################################
# Variables
################################################################################
# add commando modules here
_CMD_MODULS = [
    cmd_export,
    cmd_import,
    cmd_search,
    cmd_login,
    cmd_print,
    cmd_custom # add your command module to the module list
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
    WARNING_CSV_OPTION_WRONG       = 1
    WARNING_UNKNOWN_FILE_EXTENSION = 2
    WARNING_INFO_FILE_EXPIRED      = 3

```

</p>
</details>

## Examples

### JSON example file

  With version v1 the genereated JSON files will have following format:

```ticket.json```

```json
{
    "issue_key" : "ISSUE-TEST-1043",
    "project" : "ISSUE-TEST",
    "duedate" : "08-23-2024",
    "assignee" : "somebody else",
}
```

  In further versions this might change with the possibilty for the user to provide file templates on how JSON or CSV files shall be read and written

### CSV example file

With version v1 the genereated CSV files will have following format:

```ticket.csv```

```csv
"issue_key"; "project"; "duedate"; "assignee"

"ISSUE-TEST-1043", "ISSUE-TEST", "08-23-2024", "sombody else"
```

  In further versions this might change with the possibilty for the user to provide file templates on how JSON or CSV files shall be read and written

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
