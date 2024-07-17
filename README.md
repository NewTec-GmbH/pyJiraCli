# pyJiraCli <!-- omit in toc -->

pyJiraCli is a command-line tool designed for handling Jira tickets efficiently. With pyJiraCli, you can import/export tickets to JSON files, create tickets on the server using JSON files and search for tickets based on a search string.

[![License](https://img.shields.io/badge/license-bsd-3.svg)](https://choosealicense.com/licenses/bsd-3-clause/)
[![Repo Status](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![CI](https://github.com/NewTec-GmbH/pyJiraCli/actions/workflows/ci.yml/badge.svg)](https://github.com/NewTec-GmbH/pyJiraCli/actions/workflows/ci.yml)

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
  - [Flags](#flags)
  - [Login options](#login-options)
- [Commands](#commands)
- [Examples](#examples)
- [Add a command](#add-a-command)
- [Compile into an executable](#compile-into-an-executable)
- [Used Libraries](#used-libraries)
- [Issues, Ideas And Bugs](#issues-ideas-and-bugs)
- [License](#license)
- [Contribution](#contribution)

## Overview

![overview](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/NewTec-GmbH/pyJiraCli/main/doc/uml/context.puml)

More information on the deployment and architecture can be found in the [doc](./doc/README.md) folder.

## Installation

```cmd
git clone https://github.com/NewTec-GmbH/pyJiraCli.git
cd pyJiraCli
pip install .
```

## Usage

```cmd
pyJiraCli [-h] [--profile <profile>] [-u <user>] [-p <password>] [-t <token>] [-s <server URL>] [--version] [-v] {command} {command_options}
```

### Flags

| Flag           | Description                                                                                     |
| :-----------:  | ----------------------------------------------------------------------------------------------- |
| --verbose , -v | Print full command details before executing the command. Enables logs of type INFO and WARNING. |
| --version      | Import a ticket from a JSON file.                                                               |
| --help , -h    | Show the help message and exit.                                                                 |

### Login options

There are two options for providing the server credentials to the tool:

1. Provide all credentials via Command Line arguments:
    - `--server <server URL>` is required.
    - ID using `--user <user>` and `--password <password>`
    - Instead of user and password, you can use a token with the `--token <token>` option.
2. Provide the name of a server profile using `--profile <profile>`. A profile stores the server credentials for easier reuse, and its created using the `profile` command. See [here](./doc/commands/profile.md) for more information on the profile command.

## Commands

| Command                                     | Description                                         |
| :-----------------------------------------: | --------------------------------------------------- |
|[export](./doc/commands/export.md)           | Export a ticket from a Jira Server to a JSON file.  |
|[import](./doc/commands/import.md)           | Import a ticket from a JSON file.                   |
|[search](./doc/commands/search.md)           | Search the Jira server for issues .                 |
|[print](./doc/commands/print.md)             | Print the Jira Issue details to the console.        |
|[profile](./doc/commands/profile.md)         | Add, delete or update server profiles.              |
|[get_sprints](./doc/commands/get_sprints.md) | Get raw Sprint data.                                |

## Examples

Import an issue:

```cmd
pyJiraCli --profile my_profile import ./examples/import_issues/single_issue.json
```

Check out the all the [Examples](./examples) on how to use the pyJiraCli tool.

## Add a command

If you want to add a ned command for the tool, you can find the instructions [here](./doc/add_command.md).

## Compile into an executable

It is possible to create an executable file that contains the tool and all its dependencies. "PyInstaller" is used for this.
Just run the following command on the root of the folder:

```cmd
pyinstaller --noconfirm --onefile --console --name "pyJiraCli" --add-data "./pyproject.toml;."  "./src/pyJiraCli/__main__.py"
```

## Used Libraries

Used 3rd party libraries which are not part of the standard Python package:

- [jira](https://pypi.org/project/jira/) - Python library for interacting with JIRA via REST APIs - BSD License (BSD-2-Clause).
- [colorama](https://github.com/tartley/colorama) - ANSI color support - BSD-3 License
- [toml](https://github.com/uiri/toml) - Parsing [TOML](https://en.wikipedia.org/wiki/TOML) - MIT License

## Issues, Ideas And Bugs

If you have further ideas or you found some bugs, great! Create a [issue](https://github.com/NewTec-GmbH/pyJiraCli/issues) or if you are able and willing to fix it by yourself, clone the repository and create a pull request.

## License

The whole source code is published under [BSD-3-Clause](https://github.com/NewTec-GmbH/pyJiraCli/blob/main/LICENSE).
Consider the different licenses of the used third party libraries too!

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, shall be licensed as above, without any additional terms or conditions.
