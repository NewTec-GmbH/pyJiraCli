# Get_Sprints

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
