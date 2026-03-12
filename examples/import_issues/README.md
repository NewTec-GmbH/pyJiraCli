# Import issues <!-- omit in toc -->

Importing an issue or set of issues to the Jira Server is done using the `import` command.

- [Import single issue](#import-single-issue)
- [Import multiple issues](#import-multiple-issues)
- [Import with hierarchy (sub-issues)](#import-with-hierarchy-sub-issues)
- [Import a component](#import-a-component)
  - [Creating and assigning components](#creating-and-assigning-components)

```cmd
pyJiraCli --profile my_profile import ./examples/import_issues/single_issue.json
```

Use the `--verbose` flag to receive confirmation when issues are successfully created.

The JSON file that describes the issues to be imported requires the following format:

- It must be a JSON object at the top level.
- At the top level, a `projectKey` object must exist, containing the key `key` with the Project Key of an already-existing Jira project. This script will **not** create the project, but the issues inside the project.
- At the top level, an `issues` array must be defined. This array contains one object per issue.
- Each issue **must** have an `externalId` key defined, with a reference ID for the user. This is necessary for creating sub-issues such as Sub-Tasks. It will not be sent to the Jira Server.
- Each issue **must** have an `issuetype` object defined, which contains either an `id` or the `name` of the issue type. If both are defined, the `id` will be used. Common issue types include: `Bug`, `Task`, `New Feature`, `Sub-task`, etc.
- Each issue **must** have a `summary` key defined.
- Optional fields that can be applied to the issue include:
  - `labels`: An array of label strings (e.g., `["label1", "label2"]`)
  - `components`: An array of component objects with `name` field (e.g., `[{"name": "PM"}]`)
  - Other project-specific fields required or optional, depending on project configuration
- Other fields must be added as keys to the issue object. To determine which issue types and fields are available for your project, either use the `scheme` command or contact your Jira administrator.

Note:

The `id` key for `issuetype` is not used in the examples as it can lead to errors in the test server. However it looks like this:

```json
{
  "projectKey":{
    "key":"TESTPROJ"
  },
  "issues":[
    {
      "externalId":"1",
      "issuetype":{
        "id":"5",
        "name":"Bug"
      },
      "summary":"Fix tool documentation.",
      "labels" : ["label1", "label2"]
    }
  ]
}
```

The JIRA custom fields are more difficult, because the custom field id must be known, as well as its type. If you don't know the custom field id or even which ones are custom fields, export one issue and have a look to the JSON output.

```json
{
  ...

  "issues":[
    {
      ...

      "customfield_XXXXX": {
        "value": "my value"
      }
    }
  ]
}
```

## Import single issue

See: [Single issue template](./single_issue.json)

```cmd
pyJiraCli --profile my_profile import ./examples/import_issues/single_issue.json
```

This example demonstrates the minimal structure needed to create a single issue with optional labels. The JSON structure includes:

- A project key
- An issues array with one issue object
- Required fields: `externalId`, `issuetype`, and `summary`
- Optional fields: `labels`

## Import multiple issues

See: [Multiple issue template](./multiple_issues.json)

```cmd
pyJiraCli --profile my_profile import ./examples/import_issues/multiple_issues.json
```

This example demonstrates how to import multiple issues at once. It shows:

- Multiple issue objects in the `issues` array
- Different issue types: `Bug`, `New Feature`, `Task`
- Varying usage of optional fields (some issues have labels, others don't)

## Import with hierarchy (sub-issues)

See: [Sub-issues template](./sub_issues.json)

```cmd
pyJiraCli --profile my_profile import ./examples/import_issues/sub_issues.json
```

This example demonstrates how to create parent-child issue hierarchies. Key points:

- Sub-issues **must** have a corresponding issue type that supports sub-issues (e.g., `Sub-task`).
- Sub-issues **must** have a `parent` object defined with **either**:
  - `externalId`: When the parent issue is also created by this import file (reference the parent's externalId)
  - `key`: When the parent issue already exists in JIRA (use the existing issue key like `BUG-123`)
- Parent and child issues are included in the same `issues` array

## Import a component

See: [Component template](./component.json)

```cmd
pyJiraCli --profile my_profile import ./examples/import_issues/component.json
```

### Creating and assigning components

**Create new components** by adding a `components` array at the top level:

```json
{
  "projectKey": {"key": "PROJGR"},
  "components": [
    {
      "name": "PM",
      "description": "Project Management"
    }
  ],
  "issues": [...]
}
```

- Component `name` and `description` are required.
- If a component with the same name already exists, the creation will be skipped.

**Assign components to issues** by adding a `components` array to the issue object:

```json
"components": [
  {"name": "PM"},
  {"name": "Development"}
]
```

- If a referenced component does not exist, the import will fail.
- Ensure components are created before (or at the same time as) the issues that reference them.
