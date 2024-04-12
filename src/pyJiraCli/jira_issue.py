import os
import json
import jira_server as server
import errors

class JiraIssue:
    """Class contains all jira ticket information"""

    def __init__(self) -> None:
        self._issue_key              = None
        self._project_key            = None
        self._summary                = None
        self._desription             = None
        self._issiuetype             = None
        self._priority               = None
        self._duedate                = None
        self._assignee               = None
        self._creator                = None
        self._timeestimatedtotal     = None
        self._timeestimatedremaining = None
        self._environment            = None
        self._status                 = None

        self._labels     = []
        self._components = []
        self._versions   = []
        self._solutions  = []

    def export_issue(self, args):
        """export issue from jira server"""

        jira = server.login(args.user, args.pw)

        print(args.issue)

        try:
            issue = jira.issue(args.issue)

        except Exception as e:
            errors.prerr(e)
            return -1

        self._issue_key = issue.key
        self._project_key = issue.fields.project.key
        self._summary = issue.fields.summary
        self._desription = issue.fields.description
        self._issiuetype = issue.fields.issuetype.id
        self._priority = issue.fields.priority.id
        self._duedate = issue.fields.duedate
        self._assignee = issue.fields.assignee.displayName
        self._creator = issue.fields.creator.displayName
        self._timeestimatedtotal = issue.fields.timeoriginalestimate
        self._timeestimatedremaining = issue.fields.timeestimate
        self._environment = issue.fields.environment
        self._status = issue.fields.status.name
        
        for label in issue.fields.labels:
            self._labels.append(label)
        for component in issue.fields.components:
            self._components.append(component.name)
        for version in issue.fields.versions:
            self._versions.append(version.name)
        for solution in issue.fields.fixVersions:
            self._solutions.append(solution.name)
        
        return 0

    def import_issue(self, args):
        """"import issue from json file"""

        jira = server.login(args.user, args.pw)
        
        # get issue information from json file

    
    def print_issue(self):
        """"print issue information containend in class instance"""

    
    def create_json(self, args):
        """"write issue information in class instance to json file"""

        issue_dict = {
            'issue_key'              : self._issue_key,
            'project_key'            : self._project_key,
            'summary'                : self._summary,
            'description'            : self._desription,
            'issuetype'              : self._issiuetype,
            'priority'               : self._priority,
            'duedate'                : self._duedate,
            'assignee'               : self._assignee,
            'creator'                : self._creator,
            'timeestimatedtotal'     : self._timeestimatedtotal,
            'timeestimatedremaining' : self._timeestimatedremaining,
            'environment'            : self._environment,
            'status'                 : self._status,
            'labels'                 : self._labels,
            'components'             : self._components,
            'versions'               : self._versions,
            'solutions'              : self._solutions
        }

        if args.csv:
            print("save file in csv format")

        else:
            # Serializing json
            json_object = json.dumps(issue_dict, indent=4)
            path = args.dest

            if path is None:
                # Writing to sample.json
                with open(f'{self._issue_key}.json', "w", encoding='utf-8') as outfile:
                    outfile.write(json_object)

            else:
                # check if provided path or file is viable
                if os.path.exists(path):

                    # check if its a path to a file or a folderss
                    if os.path.isfile(path):

                        # check for file extension
                        ext = os.path.splitext(path)[-1]
                        if ext == '.json':
                            print("file extension is json")
                            file_path = path

                        else:
                            errors.prerr("wrong fileformat provided")

                    else:
                        # folder to save files was provided
                        file_path = os.path.join(path, f'{self._issue_key}.json')

                    with open(file_path, "w", encoding='utf-8') as outfile:
                        outfile.write(json_object)

                else:
                    errors.prerr("Path or file doesnt exist")

    def create_ticket(self):
        """create jira issue with information from class instance"""
