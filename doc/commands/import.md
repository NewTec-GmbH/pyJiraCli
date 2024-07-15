# Import

Import a ticket from a JSON file.
Creates a Jira issue on the server with the ticket data specified in the file.

```cmd
pyJiraCli import --help
```

Output:

```cmd
usage: pyJiraCli import [-h] file

positional arguments:
  file        Path to the input file.

options:
  -h, --help  show this help message and exit
```

Example:

```cmd
pyJiraCli import important_issue.json
```

This creates an issue on the Jira server using the data specified in `important_issue.json`.

More examples can be found in [the examples folder](./examples/import_issues/README.md).
