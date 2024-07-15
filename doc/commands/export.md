# Export

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
