from jira import JIRA

jira = JIRA('https://jira.newtec.zz/secure/Dashboard.jspa', )

issue = jira.issue('K11123P25-12')

print(issue.fields.project.key)            # 'JRA'
print(issue.fields.issuetype.name)         # 'New Feature'
print(issue.fields.reporter.displayName)   # 'Mike Cannon-Brookes [Atlassian]'