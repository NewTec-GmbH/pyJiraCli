# Profile

Add, list, delete or update server profiles.

The profile contains the following data:

* name: A unique name by which the profile can be referenced. The name is not stored in the data files, but identifies the folder. (required)
* server: The server URL to the Jira server. (required)
* token: An API token to allow for easier access. (optional)
* user/password: The credentials to authenticate with the Jira server in case no token is given. (optional)
* certificate: A server certificate for your company/Jira instance. (optional)

When adding a profile, the server URL and token (or user/password) are required.
The certificate is optional and can also be added later on with the --update option.

```cmd
pyJiraCli profile add --help
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
pyJiraCli profile add -pt jira -s https://my-jira-instance.com -t This-Is-an-Example-Token profile --cert C:\\Path\\To\\Certificate.crt new_profile
```

This will create a new Jira profile with the name "new_profile".
