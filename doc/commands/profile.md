# Profile

Add, list, delete or update server profiles.

The profile contains following data:

* name: A unique profile name by which you can reference your profile. (required)
* server: The server url where your jira server is located. (required)
* token: An api token to allow for faster access. (optional)
* certificate: A server certificate for your company/jira instance. (optional)

When adding a profile, the server url and token are required.
The certificate is optional and can also be added later on,
with the --update option.
Username and password are not valid to create a profile for security reasons.

```cmd
pyJiraCli profile add --help
```

Output:

```cmd
usage: pyJiraCli profile add [-h] -t <token> -s <server URL> [--cert <certificate path>] <profile name>

positional arguments:
  <profile name>        The name of the profile.

optional arguments:
  -h, --help            show this help message and exit
  -t <token>, --token <token>
                        The token to authenticate with the Jira server.
  -s <server URL>, --server <server URL>
                        The Jira server URL to connect to.
  --cert <certificate path>
                        The server SSL certificate.
```

Example:

```cmd
pyJiraCli profile add --server https://my-jira-instance.com --token This-Is-an-Example-Token profile --cert C:\\Path\\To\\Certificate.crt new_profile
```

This will create a new profile with the name "new_profile" and saves all possible profile information.
