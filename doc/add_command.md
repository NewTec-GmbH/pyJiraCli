# Add a command

In order to add a new command to the program, the following steps must be taken:
All added command modules must provide an "execute()" and a "register()" function.

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
                                is set on the command line \
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

3. Import ```ret.py``` and add further error codes and messages if needed.

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
    RET_ERROR_WRONG_FILE_FORMAT      = 4
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
