import jira_issue

# subparser for the 'export'command
def register(subparser):
    """register subparser commands for the export module"""
    sb_export = subparser.add_parser('export', help="export jira issue to json file")
    sb_export.add_argument('issue', type=str, help="issue key")
    sb_export.add_argument('-user', type=str, help="jira usertname if not provided with set_login")
    sb_export.add_argument('-pw', type=str, help="jira password if not provided with set_login")
    sb_export.add_argument('-dest', type=str, help="Destination for the output file")
    sb_export.add_argument('-csv',  action='store_true', help="save data in csv file format")
    sb_export.set_defaults(func=export_data)

######################################################
## export command function                          ##
######################################################
def export_data(args):
    """"export jira issue from server to json file"""
    
    issue = jira_issue.JiraIssue()
    
    # export issue from jira server
    issue.export_issue(args)

    # create json file at destination
    issue.create_json(args)

######################################################