# Profile

Add, delete or update server profiles.

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
pyJiraCli profile --help
```

Output:

```cmd
usage: pyJiraCli profile [-h] [--cert <certificate path>] (--add | --remove | --update) <profile name>

options:
  -h, --help            show this help message and exit

Profile Data:
  <profile name>        The Name under which the profile will be saved.
  --cert <certificate path>
                        The server SSL certificate.

profile operations:
  Only one operation type can be processed at a time.

  --add, -a             Add a new server profile.
  --remove, -r          Delete an existing server profile.
  --update, -u          Update an existing server profile with new data.
```

Example:

```cmd
pyJiraCli --server https://my-jira-instance.com --token This-Is-an-Example-Token profile --add new_profile --cert C:\\Path\\To\\Certificate.crt 
```

This will create a new profile with the name "new_profile" and saves all possible profile information.
