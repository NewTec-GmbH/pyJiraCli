# Search

Command to search for Jira tickets using the `search` command with a specified filter.

```cmd
pyJiraCli --profile my_profile search "project=MYPROJ"
```

You can try it by executing [example batch file](./search.bat) or [example bash file](./search.sh). Please mind to adapt the variables prior to the execution.

## Filter options

The [JQL](https://www.atlassian.com/software/jira/guides/jql/) (Jira Query Language) filter string to search for issues.

```cmd
pyJiraCli --profile my_profile search "project=MYPROJ AND reporter=MYNAME order by created desc"
```

## Limit search results

The optional argument ```[--max <MAX>]``` limits the number of issues to be returned. Default is 50.

```cmd
pyJiraCli --profile my_profile search "project=MYPROJ" --max 5 
```

## Save search results

The optional argument ```[--file <FILEPATH>]``` specifies that the search results shall be saved in the specified path to the JSON file.

```cmd
pyJiraCli --profile my_profile search "project=MYPROJ" --file .\my_search_results.json
```
