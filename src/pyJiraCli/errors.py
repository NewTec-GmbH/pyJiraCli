CRED = '\033[91m'
CEND = '\033[0m'

def prerr(error):
    """"print exit error"""
    print(CRED, "Error: ", error, CEND)
    print("error end")
