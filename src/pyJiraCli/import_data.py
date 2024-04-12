import jira_issue

# subparser for the 'import' command
def register(subparser):
    """register subparser commands for the import module"""
    sb_import = subparser.add_parser('import', help="import jira issue from json file")
    sb_import.add_argument('file', type=str, nargs='+', help="file path to the json file")
    sb_import.add_argument('-user', type=str, help="jira username if not provided with set_login")
    sb_import.add_argument('-pw', type=str, help="jira password if not provided with set_login")
    sb_import.set_defaults(func=import_data)

######################################################
## import command function                          ##
######################################################
def import_data(args):
    """import jira issue from json file"""

    issue = jira_issue.JiraIssue()

    issue.import_issue(args.file)
    issue.create_ticket()
######################################################