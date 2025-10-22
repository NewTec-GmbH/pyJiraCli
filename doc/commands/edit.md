# Scheme

Command for the edit function. Read issue information from a JSON file and edits the imported data to an existing Jira issues.

```cmd
pyJiraCli edit --help
```

Output:

```cmd
usage: pyJiraCli edit [-h] [--profile <profile>] [-u <user>] [-p <password>] [-t <token>] [-s <server URL>] file

positional arguments:
  file                  Path to the input file.

options:
  -h, --help            show this help message and exit
  --profile <profile>   The name of the server profile which shall be used for this process.
  -u <user>, --user <user>
                        The user to authenticate with the Jira server.
  -p <password>, --password <password>
                        The password to authenticate with the Jira server.
  -t <token>, --token <token>
                        The token to authenticate with the Jira server.
  -s <server URL>, --server <server URL>
                        The Jira server URL to connect to.
```

Example:

```cmd
pyJiraCli edit --profile <profile_name> toBeChanged.json
```

See `examples\edit\edit_issues.json` for an example input file.
