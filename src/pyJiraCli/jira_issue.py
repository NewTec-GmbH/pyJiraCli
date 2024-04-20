"""Jira issue Class.
   this Class contains all issue information
   provides functions to load issues from json and csv files or 
   from server with prodived issue key
   imported issues can be stored in json and csv files or written back to 
   the server
   """

# BSD 3-Clause License
#
# Copyright (c) 2024, NewTec GmbH
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

################################################################################
# Imports
################################################################################
import json
import csv
import ast
from jira import exceptions as ex

from pyJiraCli.retval import Ret
from pyJiraCli import issue_constants as _const
################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################
class JiraIssue:
    """Class contains all jira ticket information"""

    def __init__(self) -> None:
        self._issue_dictionary = {}

        for field in _const.ISSUE_FIELDS:
            if field in _const.LIST_FIELDS:
                self._issue_dictionary[field] = []
            else:
                self._issue_dictionary[field] = None

    def get_key(self):
        """return the issue key of current issue"""
        return self._issue_dictionary['issue_key']

    def export_issue(self, jira, issue:str):
        """ export issue from jira server
            
            param:
            jira: jira obj for restAPi connection with server
            issue: the issue key in string format
            
            return:
            teh exit code of the process"""

        try:
            issue = jira.issue(issue)

        except ex.JIRAError as e:
            print(e)
            return Ret.RET_ERROR_ISSUE_NOT_FOUND

        self._issue_dictionary['issue_key'] = issue.key
        self._issue_dictionary['project_key'] = issue.fields.project.key

        self._issue_dictionary['summary'] = issue.fields.summary

        self._issue_dictionary['description'] = issue.fields.description

        if issue.fields.issuetype is not None:
            self._issue_dictionary['issuetype'] = issue.fields.issuetype.id

        if issue.fields.priority is not None:
            self._issue_dictionary['priority'] = issue.fields.priority.name

        self._issue_dictionary['duedate'] = issue.fields.duedate

        if issue.fields.assignee is not None:
            self._issue_dictionary['assignee'] = issue.fields.assignee.name

        if issue.fields.creator is not None:
            self._issue_dictionary['creator'] = issue.fields.creator.displayName

        self._issue_dictionary['creation_date'] = issue.fields.created

        self._issue_dictionary['timeestimatedtotal'] = issue.fields.timeoriginalestimate

        self._issue_dictionary['timeestimatedremaining'] = issue.fields.timeestimate

        self._issue_dictionary['environment'] = issue.fields.environment

        if issue.fields.status is not None:
            self._issue_dictionary['status'] = issue.fields.status.name

        for label in issue.fields.labels:
            self._issue_dictionary['labels'].append(label)
        for component in issue.fields.components:
            self._issue_dictionary['components'].append(component.name)
        for version in issue.fields.versions:
            self._issue_dictionary['versions'].append(version.name)
        for solution in issue.fields.fixVersions:
            self._issue_dictionary['solutions'].append(solution.name)

        return Ret.RET_OK

    def import_issue(self, dictonary):
        """ import issue from dictionary

            param:
            dictionary: a python dictionary conatining jira issue info
            """

        # get issue information from json or csv file
        for field in dictonary:
            if field in _const.ISSUE_FIELDS:
                if field in _const.LIST_FIELDS:
                    self._issue_dictionary[field] = ast.literal_eval(dictonary[field])
                else:
                    self._issue_dictionary[field] = dictonary[field]

    def print_issue(self):
        """"print issue information containend in class instance"""

    def create_json(self, file_path):
        """ write issue information in class instance to a json file
            
            param: 
            file_path: path to the json file 
            
            return:
            the exit status of the process
        """

        # serialize json object
        json_object = json.dumps(self._issue_dictionary, indent=4)

        try:
            with open(file_path, "w", encoding='utf-8') as outfile:
                outfile.write(json_object)

        except (OSError, IOError) as e:

            # print exception
            print(e)
            return Ret.RET_ERROR_FILE_OPEN_FAILED

        return Ret.RET_OK

    def create_csv(self, file_path):
        """ write issue information in class instance to a csv file
            
            param: 
            file_path: path to the csv file 
            
            return:
            the exit status of the process
        """
        try:
            with open(file_path, "w", encoding='utf-8') as outfile:
                csv_writer = csv.DictWriter(outfile,  delimiter=';', fieldnames=_const.ISSUE_FIELDS)

                csv_writer.writeheader()
                csv_writer.writerow(self._issue_dictionary)

        except (OSError, IOError) as e:
            # print exception
            print(e)
            return Ret.RET_ERROR_FILE_OPEN_FAILED

        return Ret.RET_OK


    def create_ticket(self, jira):
        """ create jira issue on the server with information from class instance
        
            param: 
            jira: jira obj for restAPi connection with server
            
            return:
            the exit status of the process
        """

        write_dictionary = self._create_write_dictionary()

        try:
            jira.create_issue(fields=write_dictionary)

        except ex.JIRAError as e:
            print(e)
            return Ret.RET_ERROR_CREATING_TICKET_FAILED

        return Ret.RET_OK


    def _create_write_dictionary(self):

        write_dictonary = {}

        for field in _const.ISSUE_FIELDS:
            if self._issue_dictionary[field] is not None or self._issue_dictionary[field] == []:

                if field == 'project_key':
                    write_dictonary['project'] = {"key" : self._issue_dictionary['project_key']}

                elif field == 'summary':
                    write_dictonary["summary"] = self._issue_dictionary['summary']

                elif field == 'description':
                    write_dictonary["description"] = self._issue_dictionary['description']

                elif field == 'issuetype':
                    write_dictonary["issuetype"] = \
                        _const.ISSUE_TYPES[self._issue_dictionary['issuetype']]

                elif field == 'priority':
                    write_dictonary['priority'] = {"name" : self._issue_dictionary['priority']}

                elif field == 'duedate':
                    write_dictonary['duedate'] = self._issue_dictionary['duedate']

                elif field == 'assignee':
                    write_dictonary['assignee'] = {"name" : self._issue_dictionary['assignee']}

                else:
                    pass

#                    case 'timeestimatedtotal':
#                        write_dictonary['timeestimatedtotal'] =
#                           self._issue_dictionary['timeestimatedtotal']

#                    case 'timeestimatedremaining':
#                        write_dictonary['timeestimatedremaining'] =
#                            self._issue_dictionary['timeestimatedremaining']

#                    case 'environment':
#                        write_dictonary['environment'] = self._issue_dictionary['environment']

#                    case 'labels':
#                        write_dictonary['labels'] = self._issue_dictionary['labels']

#                    case 'components':
#                        write_dictonary['components'] =
#                            {"key" : self._issue_dictionary['project_key']}

#                    case 'versions':
#                        write_dictonary['versions'] =
#                            {"key" : self._issue_dictionary['project_key']}

#                    case 'solutions':
#                        write_dictonary['solutions'] =
#                            {"key" : self._issue_dictionary['project_key']}
        return write_dictonary
