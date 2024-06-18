# Get_sprints

Command to search for Sprints using the `get_sprints` command on a specified board.

```cmd
pyJiraCli --profile my_profile get_sprints "MY_BOARD"
```

## Specify output file

The optional argument ```[--file <FILEPATH>]``` specifies that the results shall be saved in the specified path to the JSON file.
Otherwise the file will be stored in the current working directory.
```cmd
pyJiraCli --profile my_profile search "project=MYPROJ" --file .\my_sprints.json
```

## Example
For an example of the command output check [here](./sprints_in_board.json).