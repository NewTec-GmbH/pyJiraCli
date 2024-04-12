######################################################
## register module in parser                        ##
######################################################
def register(subparser):
    """register subparser commands for the search module"""
    # subparser for the 'search' command
    sb_search = subparser.add_parser('search', help="search for jira issues with specified filter string")
    sb_search.add_argument('filter', type=str, help="filter string according to which issue are to be searched")
    sb_search.add_argument('-user', type=str, help="jira usertname if not provided with set_login")
    sb_search.add_argument('-pw', type=str, help="jira password if not provided with set_login")
    sb_search.set_defaults(func=search)
######################################################

######################################################
## search command function                          ##
######################################################
def search(args):
    print(f"searching for issues with filter {args.filter}")
######################################################