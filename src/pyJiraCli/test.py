from jira import JIRA
import certifi
import os

os.environ["SSL_CERT_FILE"] = certifi.where()
jira = JIRA(server="https://jira.newtec.zz", basic_auth=("heitzmann", "Iajss24MhbNT!"), options={"verify": False})
jira.verify_ssl = False

issue = jira.issue("K11001JIRASCHUL-1213")

_issue_key = issue.key
_project_key = issue.fields.project.key
_summary = issue.fields.summary
_desription = issue.fields.description
_issiuetype = issue.fields.issuetype.id
_priority = issue.fields.priority.id
_duedate = issue.fields.duedate
_assignee = issue.fields.assignee.displayName
_creator = issue.fields.creator.displayName
_timeEstimatedTotal = issue.fields.timeoriginalestimate
_timeEstimatedRemaining = issue.fields.timeestimate 
_environment = issue.fields.environment

_labels = []
for label in issue.fields.labels:
    _labels.append(label)

_components = []
for component in issue.fields.components:
    _components.append(component.name)

_version = []
for version in issue.fields.versions:
    _version.append(version.name)

_solution = [] 
for fix in issue.fields.fixVersions:
    _solution.append(fix.name)

issue_dict = {
    "project" : {"key" : "K11001JIRASCHUL"},
    "summary" : "new critical Task from pyJiraCli",
    "description" : "this is a test to create an issue from the pyJiraCli tool",
    "issuetype" : "Aufgabe",
    "priority" : {'name' : 'Critical'}
}

# jira.create_issue(fields=issue_dict)
