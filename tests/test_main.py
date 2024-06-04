"""
Tests for the pyJiraCli command line interface.
"""

import subprocess

PYTHON_EXECUTABLE = "python"
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
    args = [PYJIRACLI_EXECUTABLE]
    args.extend(arguments)

    return subprocess.run(args,
                          # Capture stdout and stderr.
                          capture_output=True,
                          # Do not raise exception on non-zero exit code.
                          check=False,
                          shell=False)  # Run command in shell.


def test_help():
    """
    Test the help argument of the pyJiraCli and all its commands.
    """

    # Test the help argument of the pyJiraCli.
    ret = run_pyjiracli(["--help"])
    assert ret.returncode == 0

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
        assert ret.returncode == 0
