# pyJiraCli <!-- omit in toc -->

pyJiraCli is a command-line tool designed for handling Jira tickets efficiently. With pyJiraCli, you can import/export tickets to JSON/CSV files, create tickets on the server using JSON/CSV files and search for tickets based on a search string.

[![License](https://img.shields.io/badge/license-bsd-3.svg)](https://choosealicense.com/licenses/bsd-3-clause/)
[![Repo Status](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
![CI Status](https://github.com/NewTec-GmbH/pyJiraCli/actions/workflows/test.yml/badge.svg)

* [Installation](#installation)
* [Overview](#overview)
* [Usage](#usage)
    * [Commands](#commands)
        * [export](#export)
        * [import](#export)
        * [login](#login)
        * [search](#search)
        * [print](#print)
    * [Add a command](#custom-cmds)
* [Examples](#examples)
    * [Field config file](#field-config-file)
    * [json example file](#json-example-file)
    * [csv example file](#csv-example-file)
* [Used Libraries](#used-libraries)
* [Issues, Ideas And Bugs](#issues-ideas-and-bugs)
* [License](#license)
* [Contribution](#contribution)

# Installation
```cmd
$ git clone https://github.com/NewTec-GmbH/pyJiraCli.git
$ cd pyJiraCli
$ pip install .
```
# Overview
![goverview](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/NewTec-GmbH/pyJiraCli/main/design/context.puml)

# Usage
Show help information:
```cmd
$ pyJiraCli --help
```
    positional arguments:
      {export,import,search,login,print}
        export              export jira issue to json file
        import              import jira issue from json or csv file
        search              search jira issues with specified filter string
        login               save or delete login information
        print               print issue details to the console

    options:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      --verbose             print full command details before executing the command

All added command modules must provide a "execute()" and a "register()"

# Commands
## export
   export a ticket from a Jira Server to a json or csv file

```cmd
$ pyJiraCli export --help
```

    usage: pyJiraCli export [-h] [-user <username>] [-pw <password>] [-path <folder_path>] [-file <filename>] [-csv] issue

    positional arguments:
    issue                issue key

    options:
      -h, --help           show this help message and exit
      -user <username>     jira username if not provided with login
      -pw <password>       jira password if not provided with login
      -path <folder_path>  Destination for the output file
      -file <filename>     name of the output file
      -csv                 save data in csv file format

## import
  import a ticket from a json or csv file, create an online jira issue with the 
  ticket data on the server

```cmd
$ pyJiraCli import --help
```
    usage: pyJiraCli import [-h] [-user <username>] [-pw <password>] file

    positional arguments:
      file              file path to the json file

    options:
      -h, --help        show this help message and exit
      -user <username>  jira username if not provided with set_login
      -pw <password>    jira password if not provided with set_login

## login
  save login data. To login, either username and password or email and API token need to be provided.
  To store the email address use option -user and option -token

```cmd
$ pyJiraCli login --help
```

    usage: pyJiraCli login [-h] [-user <username>] [-pw <password>] [-token <API token>] [-url <server url>] [-expires <time>] [--min] [--day] [--month] [-delete] [--default] [--userinfo] [--server] [--token]

    options:
      -h, --help          show this help message and exit
      -user <username>    jira username for login
      -pw <password>      jira password for login
      -token <API token>  user API token for login authenfication
      -url <server url>   jira server for login
      -expires <time>     time after which the stored login info will expire. default = 30 days
      --min               expire time in minutes
      --day               expire time in days
      --month             expire time in months
      -delete             delete login information
      --default           delete or store default server url
      --userinfo, -ui     delete user infomation only
      --server, -s        delete server information only
      --token, -t         delete API token information only

## search 
**TODO** \
  search the jira server for issues with a filter string
    
```cmd
$ pyJiraCli search --help
```
    usage: pyJiraCli search [-h] [-user <username>] [-pw <password>] filter

    positional arguments:
      filter            filter string according to which issue are to be searched

    options:
      -h, --help        show this help message and exit
      -user <username>  jira usertname if not provided with set_login
      -pw <password>    jira password if not provided with set_login

## print 
**TODO** \
  print ticket information to the console

```cmd
$ pyJiraCli print --help
```
    usage: pyJiraCli print [-h] [-user <username>] [-pw <password>] issue

    positional arguments:
      issue             issue key

    options:
      -h, --help        show this help message and exit
      -user <username>  jira usertname if not provided with set_login
      -pw <password>    jira password if not provided with set_login
# Add a command
Further command line commands can be added 

to add a cmd module:
 * the module must provide the functions: \
 ```cmd.py``` :

    ```py
    # import the exit codes
    from pyJiraCli.retval import Ret

    def register(subparser):
      ''' register the command and its options '''

        sb_cmd = subparser.add_parser('cmd',
                                       help="a custom command")

        sb_cmd.add_argument('postional arg',
                             type=str,
                             help="some positional argument that is read as a string")

        sb_cmd.add_argument('-option',
                             type=str,
                             metavar='<username>',
                             help="some otption that reads in a string")
        
        sb_cmd.add_argument('-bool_option',
                              action="store_true",
                              help="store 'True'' in args.bool_option if the option \
                                    is set on the commandline \
                                    otehrwise store 'False'")
        
        # make sure to return the command parser
        return sb_cmd
    
    def execute(args):
      ''' execute function, your module enty point will be here
          returns the module exit code: 
          retval.Ret.RET_OK'''
        ret_status = Ret.RET_OK

        ret_status = execute_cmd(args)

        return ret_status
    ```

  
  * in ```__main__.py``` add:
  
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

    * import ```retval.py``` and add further error codes and messages if needed \
    ```retval.py```:
    ```py
    class Ret(IntEnum):
        """"exit statuses of the modules"""
        RET_OK                           = 0
        RET_ERROR                        = 1
        RET_ERROR_JIRA_LOGIN             = 2
        RET_ERROR_FILE_NOT_FOUND         = 3
        RET_ERROR_WORNG_FILE_FORMAT      = 4
        RET_ERROR_ISSUE_NOT_FOUND        = 5
        RET_ERROR_FILE_OPEN_FAILED       = 6
        RET_ERROR_NO_USERINFORMATION     = 7
        RET_ERROR_MISSING_UNSERINFO      = 8
        RET_ERROR_MISSING_ARG_INFO     = 9
        RET_ERROR_CREATING_TICKET_FAILED = 10
        RET_ERROR_INFO_FILE_EXPIRED      = 11
        RET_ERROR_CUSTOM_ERR             = 12 # custom error


    RETURN_MSG = {
        Ret.RET_OK                           : "Process succesful",
        Ret.RET_ERROR                        : "Error occured",
        Ret.RET_ERROR_JIRA_LOGIN             : "Login to jira server was not possible",
        Ret.RET_ERROR_FILE_NOT_FOUND         : "Folder or File doesn't exist",
        Ret.RET_ERROR_WORNG_FILE_FORMAT      : "Wrong file format for save file provided",
        Ret.RET_ERROR_ISSUE_NOT_FOUND        : "Jira Issue not found",
        Ret.RET_ERROR_FILE_OPEN_FAILED       : "opening File failed",
        Ret.RET_ERROR_NO_USERINFORMATION     : "no user information was provided via cli" + \
                                               "or stored information file",
        Ret.RET_ERROR_MISSING_UNSERINFO      : "both -user and -pw option must be provided " + 
                                               "to store useriformation",
        Ret.RET_ERROR_MISSING_ARG_INFO     : "At least one of the options must be" + 
                                               "provided:" +                               
                                               "(-user, -pw), -server or -delete",
        Ret.RET_ERROR_CREATING_TICKET_FAILED : "creating the ticket on the jira server" +
                                               " failed",
        Ret.RET_ERROR_INFO_FILE_EXPIRED      : "the stored information has expired"
        Ret.RET_ERROR_CUSTOM_ERR             : "error text" # custom error text,
                                                            # that will be
                                                            # displayed if,
                                                            # the tool exits with your 
                                                            # error code
    }
    ```
# Examples

## Field config file
  **TODO:** add jira field configuration and json/csv file configugration via config file templates. With that the program shall get the fileformat and fieldnames for jira with a set configuration file provided by the user. This will help making the tool able to adapt to different jira settings and configurations 

## json example file
  With version v1 the genereated json files will have following format:

```ticket.json```
```json
{
    "issue_key" : "ISSUE-TEST-1043",
    "project" : "ISSUE-TEST",
    "duedate" : "08-23-2024",
    "assignee" : "somebody else",
}
```

  In further versions this might change with the possibilty for the user to provide file templates on how json or csv files shall be read and written

## csv example file
With version v1 the genereated csv files will have following format:

```ticket.csv```
```csv
"issue_key"; "project"; "duedate"; "assignee"

"ISSUE-TEST-1043", "ISSUE-TEST", "08-23-2024", "sombody else"
```

  In further versions this might change with the possibilty for the user to provide file templates on how json or csv files shall be read and written

# Used Libraries
Used 3rd party libraries which are not part of the standard Python package:
* [jira](https://pypi.org/project/jira/) - Python library for interacting with JIRA via REST APIs - BSD License (BSD-2-Clause).
* [cryptography](https://pypi.org/project/cryptography/) - cryptography is a package which provides cryptographic recipes and primitives to Python developers. - Apache Software License, BSD License (Apache-2.0 OR BSD-3-Clause)
* [toml](https://github.com/uiri/toml) - Parsing [TOML](https://en.wikipedia.org/wiki/TOML) - MIT License


# Issues, Ideas And Bugs
If you have further ideas or you found some bugs, great! Create a [issue](https://github.com/NewTec-GmbH/pyJiraCli/issues) or if you are able and willing to fix it by yourself, clone the repository and create a pull request.

# License
The whole source code is published under [BSD-3-Clause](https://github.com/NewTec-GmbH/pyJiraCli/blob/main/LICENSE).
Consider the different licenses of the used third party libraries too!

# Contribution
Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, shall be licensed as above, without any additional terms or conditions.