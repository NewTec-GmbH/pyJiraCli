# pyJiraCli <!-- omit in toc -->

pyJiraCli is a command-line tool designed for handling Jira tickets efficiently. With pyJiraCli, you can import/export tickets from/to JSON/CSV files, create tickets on the server using JSON/CSV files, and search for tickets based on a search string.

[![License](https://img.shields.io/badge/license-bsd-3.svg)](https://choosealicense.com/licenses/bsd-3-clause/)
[![Repo Status](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
![CI Status](https://github.com/NewTec-GmbH/pyJiraCli/actions/workflows/test.yml/badge.svg)

* [Installation](#installation)
* [Overview](#overview)
* [Usage](#usage)
    * [commands](#commands)
        * [export](#export)
        * [import](#export)
        * [login](#login)
        * [search](#search)
        * [print](#print)
* [Examples](#examples)
    * [Field config file](#field-config-file)
    * [json example file](#json-example-file)
    * [csv example file](#csv-example-file)
* [Ideas](#ideas)

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
$ pyHexDump --help
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


# Commands
## export
   export a ticket from a Jira Server to a json or csv file

```cmd
$ pyHexDump export --help
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
$ pyHexDump import --help
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
$ pyHexDump login --help
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
$ pyHexDump search --help
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
$ pyHexDump print --help
```
    usage: pyJiraCli print [-h] [-user <username>] [-pw <password>] issue

    positional arguments:
      issue             issue key

    options:
      -h, --help        show this help message and exit
      -user <username>  jira usertname if not provided with set_login
      -pw <password>    jira password if not provided with set_login

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

# Ideas
&cross; add file templates for json and csv files \
&cross; provide jira field configuraion via a config file \
&cross; add security to login data storage (currently logindata is encrypted and the encryption key is encrypted with a device unique key) \
&cross; implement search command  
&cross; implement print command  