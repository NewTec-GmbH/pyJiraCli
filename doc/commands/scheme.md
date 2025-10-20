# Scheme

Command to retrieve the scheme of the Jira server. Retrieves the issue types and fields for the Jira instance, or for an specific project if the `--project` argument is supplied.

```cmd
pyJiraCli scheme --help
```

Output:

```cmd
usage: pyJiraCli scheme [-h] [--profile <profile>] [-u <user>] [-p <password>] [-t <token>] [-s <server URL>] [--project <project>]

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
  --project <project>   The name of the project to get the scheme information for.
```

Examples:

```cmd
pyJiraCli scheme --profile <profile_name>
```

Creates file `scheme_output.json`.

```cmd
pyJiraCli scheme --profile <profile_name> --project <project_id>
```

Creates file `scheme_output_<project_id>.json.json`.
