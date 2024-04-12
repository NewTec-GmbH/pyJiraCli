import os
import certifi

from jira import JIRA
import set_login
import errors

def login(user, pw):
    """"login to jira server with user info or user info from file"""
    
    if user is None or pw is None:
        # get login information from login module
        user, pw = set_login.decrypt_login_info()

    try:
        os.environ["SSL_CERT_FILE"] = certifi.where()
        jira = JIRA(server="https://jira.newtec.zz", basic_auth=(user, pw), options={"verify": False})
        jira.verify_ssl = False
        return jira

    except Exception as e:
        #print error
        errors.prerr(e)
