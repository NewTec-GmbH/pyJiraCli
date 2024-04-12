# subparser for the 'print' command
def register(subparser):
    """register subparser commands for the print_issue module"""
    sb_search = subparser.add_parser('print', help="print issue details to the console")
    sb_search.add_argument('issue', type=str, help="issue key")
    sb_search.add_argument('-user', type=str, help="jira usertname if not provided with set_login")
    sb_search.add_argument('-pw', type=str, help="jira password if not provided with set_login")
    sb_search.set_defaults(func=print_details)

######################################################
## print command function                           ##
######################################################
def print_details(args):
    print(f'print details for issue {args.issue}')
######################################################