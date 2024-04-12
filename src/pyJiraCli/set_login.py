# subparser for the 'set_login' command
def register(subparser):
    """register subparser commands for the set_login module"""
    sb_login = subparser.add_parser('set_login', help="save login information")
    sb_login.add_argument('-user', type=str, help="jira username for login")
    sb_login.add_argument('-pw', type=str, help="jira password for login")
    sb_login.add_argument('-delete', action='store_true', help="delete login information")
    sb_login.set_defaults(func=set_login)

######################################################
## set_login command function                       ##
######################################################
def set_login(args):
    
    if args.delete:
        delete_login_file()
    
    else:
        encrypt_login_info(args.user, args.pw)
######################################################

def encrypt_login_info(user, pw):
    print("decrypt login info")
    
def decrypt_login_info():
    user = None
    pw = None

    return user, pw

def delete_login_file():
    print("delete login file")