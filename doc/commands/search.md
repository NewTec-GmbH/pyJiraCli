# Search

Search the Jira server for issues using the specified filter string. The string must be in JQL (Jira Query Language) format.

If you need help working with filters, check out <https://confluence.atlassian.com/jirasoftwareserver/advanced-searching-939938733.html>.
Also, the results can be ordered by command, just add "order by" to your cmd

```cmd
pyJiraCli search --help
```

Output:

```cmd
usage: pyJiraCli search [-h] [--max <MAX>] [--file <PATH TO FILE>] [--full] [--field <field>] filter

positional arguments:
  filter                Filter string to search for. Must be in JQL format.

options:
  -h, --help            show this help message and exit
  --max <MAX>           Maximum number of issues that may be found.Default is 50.If set to 0, all issues will be searched.
  --file <PATH TO FILE>
                        Absolute filepath or filepath relative to the current work directory to a JSON file.
  --full                Get the full information of the issues. Can be slow in case of many issues.
  --field <field>       The field to search for in the issues. Can be used multiple times to search for multiple fields.
```

Example:

```cmd
pyJiraCli search --max 50 "project=PROJ order by created desc" --field issuetype
```

This will find the 50 latest issues in project PROJ and display them by descending creation date. The only information displayed will be the `key` and the `issuetype`.

More examples can be found in [the examples folder](./examples/search/README.md).
