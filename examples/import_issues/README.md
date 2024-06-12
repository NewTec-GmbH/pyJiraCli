# Import issues

Importing an issue or set of issues to the Jira Server is done using the `import` command.

```cmd
pyJiraCli --profile my_profile import .\examples\import_issues.json\single_issue.json
```

Use the `--verbose` flag to receive confirmation when issues are successfully created.

The JSON file that describes the issues to be imported requires the following format:

- It must be a JSON object at the top level.
- At the top level, a `projectKey` object must exist, containing the key `key` with the Project Key of an already-existing Jira project. This script will **not** create the project, but the issues inside the project.
- At the top level, an `issues` array must be defined. This array contains one object per issue.
- Each issue **must** have an `externalId` key defined, with a reference ID for the user. This is necessary for creating sub-issues such as Sub-Tasks. It will not be sent to the Jira Server.
- Each issue **must** have an `issuetype` object defined, which contains either an `id` or the `name` of the issue type. If both are defined, the `id` will be used.
- Each issue **must** have a `summary` key defined.
- Other fields that can be applied to the issue, required or optional, must be defined by the user depending on the project. This is done by adding more keys to the issue object.
- To determine which issue types and fields are available, please contact your Jira administrator.

## Import single issue

See: [Single issue template](./single_issue.json)

```cmd
pyJiraCli --profile my_profile import .\examples\import_issues.json\single_issue.json
```

The `labels` array is an optional field.

## Import multiple issues

See: [Multiple issue template](./multiple_issues.json)

```cmd
pyJiraCli --profile my_profile import .\examples\import_issues.json\multiple_issues.json
```

## Import sub-issues

See: [Sub-issues template](./sub_issues.json)

```cmd
pyJiraCli --profile my_profile import .\examples\import_issues.json\sub_issues.json
```

- Sub-issues must have a corresponding Sub-Issue/Task type.
- Sub-issues **must** have a `parent` object defined, which contains either the `externalId` or the `key` of their parent issue.
- The `externalId` key shall be used when the parent issue is also being created by this import file.
- The `key` key shall be used when the issue already exists (it was not created with this import file.)
