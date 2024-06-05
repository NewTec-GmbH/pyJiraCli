"""
Tests for the pyJiraCli command line interface.
"""

import subprocess
from pyJiraCli.ret import Ret

# The command must already be installed in the environment.
PYJIRACLI_EXECUTABLE = "pyJiraCli"


def run_pyjiracli(arguments) -> object:
    """
    Wrapper to run pyJiraCli command line.

    Args:
        arguments (list): List of arguments to pass to pyJiraCli.

    Returns:
        subprocess.CompletedProcess[bytes]: The result of the command. 
        Includes return code, stdout and stderr.

    """
    args = [PYJIRACLI_EXECUTABLE]  # The executable to run.
    args.extend(arguments)  # Add the arguments to the command.

    return subprocess.run(args,
                          # Capture stdout and stderr.
                          capture_output=True,
                          # Do not raise exception on non-zero exit code.
                          check=False,
                          # Do not run command in shell. Otherwise, it will not work on Linux.
                          shell=False)


def test_help():
    """
    Test the help argument of the pyJiraCli and all its commands.
    """

    # No arguments should return the help message.
    ret = run_pyjiracli([])
    assert Ret.RET_OK == ret.returncode  # Expect success.

    # Test the help argument of the pyJiraCli.
    ret = run_pyjiracli(["--help"])
    assert Ret.RET_OK == ret.returncode  # Expect success.

    # Get all commands of the pyJiraCli using the previous help command.
    help_message = ret.stdout.decode("utf-8")
    start_index = help_message.find("{")
    end_index = help_message.find("}")
    assert start_index != -1, help_message  # Start of command list not found.
    assert end_index != -1, help_message  # End of command list not found.

    # Extract the command list.
    command_list = help_message[start_index+1:end_index].split(",")

    # Test the help argument of all commands.
    for command in command_list:
        ret = run_pyjiracli([command, "--help"])
        assert Ret.RET_OK == ret.returncode


def test_delete():
    """
    Test the delete command of the pyJiraCli.
    """

    # Test the delete command with no arguments.
    ret = run_pyjiracli(["delete"])
    # Expect invalid arguments.
    assert Ret.RET_OK == ret.returncode, ret.stderr

    # Futher tests will be done in the future, as the command will change.


def test_export():
    """
    Test the export command of the pyJiraCli.
    """

    # Test the export command with no arguments.
    ret = run_pyjiracli(["export"])
    # Expect invalid arguments.
    assert Ret.RET_ERROR_ARGPARSE == ret.returncode, ret.stderr

    # Futher tests will be done in the future, as the command will change.


def test_import():
    """
    Test the import command of the pyJiraCli.
    """

    # Test the import command with no arguments.
    ret = run_pyjiracli(["import"])
    # Expect invalid arguments.
    assert Ret.RET_ERROR_ARGPARSE == ret.returncode, ret.stderr

    # Futher tests will be done in the future, as the command will change.


def test_login():
    """
    Test the login command of the pyJiraCli.
    """

    # Test the login command with no arguments.
    ret = run_pyjiracli(["login"])
    # Expect invalid arguments.
    assert Ret.RET_ERROR_ARGPARSE == ret.returncode, ret.stderr

    # Futher tests will be done in the future, as the command will change.


def test_print():
    """
    Test the print command of the pyJiraCli.
    """

    # Test the print command with no arguments.
    ret = run_pyjiracli(["print"])
    # Expect invalid arguments.
    assert Ret.RET_ERROR_ARGPARSE == ret.returncode, ret.stderr

    # Futher tests will be done in the future, as the command will change.


def test_search():
    """
    Test the search command of the pyJiraCli.
    """

    # Test the search command with no arguments.
    ret = run_pyjiracli(["search"])
    # Expect invalid arguments.
    assert Ret.RET_ERROR_ARGPARSE == ret.returncode, ret.stderr

    # Futher tests will be done in the future, as the command will change.
