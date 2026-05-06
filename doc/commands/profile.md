# Profile

- [Add](#add)
- [List](#list)
- [Remove](#remove)
- [Update](#update)
- [Show](#show)

Add, list, remove, update or show server profiles.

The profile contains the following data:

- name: A unique name by which the profile can be referenced. The name is not stored in the data files, but identifies the folder. (required)
- server: The server URL to the Jira server. (required)
- token: An API token to allow for easier access. (optional)
- user/password: The credentials to authenticate with the Jira server in case no token is given. (optional)
- certificate: A server certificate for your company/Jira instance. (optional)

When adding a profile, the server URL and token (or user/password) are required.
The certificate is optional and can also be added later on with the `update` subcommand.

```cmd
pyJiraCli profile [-h] {add,list,remove,update,show} ...
```

## Add

Add a new Jira server profile.

```cmd
pyJiraCli profile add [-h] -s <server URL> [-t <token>] [-u <user>] [-p <password>] [--cert <certificate path>] <profile name>
```

Output:

```cmd
usage: pyJiraCli profile add [-h] -s <server URL> [-t <token>] [-u <user>] [-p <password>] [--cert <certificate path>] <profile name>

positional arguments:
  <profile name>        The name of the profile.

options:
  -h, --help            show this help message and exit
  -s <server URL>, --server <server URL>
                        The Jira server URL to connect to.
  -t <token>, --token <token>
                        The token to authenticate at the Jira server.
  -u <user>, --user <user>
                        The user to authenticate at the Jira server.
  -p <password>, --password <password>
                        The password to authenticate at the Jira server.
  --cert <certificate path>
                        The server SSL certificate.
```

Example:

```cmd
pyJiraCli profile add -s https://my-jira-instance.com -t This-Is-an-Example-Token --cert C:\\Path\\To\\Certificate.crt new_profile
```

This will create a new Jira profile with the name "new_profile":

```cmd
Successfully created profile 'new_profile'.
```

## List

List the names of all stored Jira profiles.

```cmd
pyJiraCli profile list [-h]
```

Output:

```cmd
usage: pyJiraCli profile list [-h]

options:
  -h, --help  show this help message and exit
```

Example:

```cmd
pyJiraCli profile list
```

This will print the names of all stored profiles:

```cmd
Profiles:
    new_profile
```

## Remove

Remove an existing profile.

```cmd
pyJiraCli profile remove [-h] <profile name>
```

Output:

```cmd
usage: pyJiraCli profile remove [-h] <profile name>

positional arguments:
  <profile name>  The name of the profile.

options:
  -h, --help      show this help message and exit
```

Example:

```cmd
pyJiraCli profile remove new_profile
```

This will remove the profile "new_profile":

```cmd
Successfully removed profile 'new_profile'.
```

## Update

Update the certificate of an existing profile.

```cmd
pyJiraCli profile update [-h] [-s <server URL>] [-t <token>] [-u <user>] [-p <password>] [-c <certificate path>] <profile name>
```

Output:

```cmd
usage: pyJiraCli profile update [-h] [-s <server URL>] [-t <token>] [-u <user>] [-p <password>] [-c <certificate path>] <profile name>

positional arguments:
  <profile name>        The name of the profile.

options:
  -h, --help            show this help message and exit
  -s <server URL>, --server <server URL>
                        The Jira server URL to connect to.
  -t <token>, --token <token>
                        The token to authenticate with the Jira server.
  -u <user>, --user <user>
                        The user to authenticate at the Jira server.
  -p <password>, --password <password>
                        The password to authenticate at the Jira server.
  -c <certificate path>, --cert <certificate path>
                        The server SSL certificate.
```

Example:

```cmd
pyJiraCli profile update -c C:\\Path\\To\\Certificate.crt new_profile
```

This will add or replace the certificate of the profile "new_profile":

```cmd
Successfully added certificate to profile 'new_profile'.
```

## Show

Print all stored data of an existing profile.

```cmd
pyJiraCli profile show [-h] <profile name>
```

Output:

```cmd
usage: pyJiraCli profile show [-h] <profile name>

positional arguments:
  <profile name>  The name of the profile.

options:
  -h, --help      show this help message and exit
```

Example:

```cmd
pyJiraCli profile show new_profile
```

This will print the details of the profile "new_profile":

```cmd
Profile name: new_profile
Profile type: jira
Server URL:   https://my-jira-instance.com
Token:        This-Is-an-Example-Token
Certificate:  C:\Path\To\Certificate.crt
```
