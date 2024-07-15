# Print

Print the Jira Issue details to the console.

```cmd
pyJiraCli print --help
```

Output:

```cmd
usage: pyJiraCli print [-h] issueKey

positional arguments:
  issueKey    The Jira Issue Key of the Issue to print.

options:
  -h, --help  show this help message and exit
```

Example:

```cmd
pyJiraCli print ISSUE-2291
```

The output depends on the fields configured by the Jira server.
