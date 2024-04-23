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
        self._issue = None

        for field in _const.ISSUE_FIELDS:
            if field in _const.LIST_FIELDS:
                self._issue_dictionary[field] = []
            else:
                self._issue_dictionary[field] = None

    def get_key(self):
        """return the issue key of current issue
        
        Returns:
            key (str):  the current issue key or None
    """

        key = None

        if 'key' in self._issue_dictionary:
            key = self._issue_dictionary['key']

        return key

    def export_issue(self, jira, issue:str):
        """load the issue from the jira server
           and store its information in the instance
           of the class 
            
        Args:
            jira (jira obj):    jira obj for restAPi connection with server
            issue (str):        the issue key in string format
            
        Returns:
            ret_status (Ret):   the exit code of the process"""
        ret_status = Ret.RET_OK

        try:
            self._issue = jira.issue(issue)

        except ex.JIRAError as e:
            print(e)
            ret_status = Ret.RET_ERROR_ISSUE_NOT_FOUND

        if ret_status == Ret.RET_OK:
            self._process_issue()

        return ret_status

    def import_issue(self, dictionary):
        """import issue from dictionary

           store all values which have a key 
           in the instances issue_dict to the
           class instance 
        
        Args:
            dictionary (dict): a python dictionary conatining jira issue info
        """

        # get issue information from json or csv file
        for field in dictionary:
            if field in _const.ISSUE_FIELDS:
                self._issue_dictionary[field] = dictionary[field]

    def print_issue(self):
        """"print issue information containend in class instance"""

    def create_json(self, file_path):
        """ write issue information in class instance to a json file
            
        Args: 
            file_path (str):    path to the json file 
            
        Returns:
            ret_status (Ret):   the exit status of the process
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
        """ write issue information in class instance to a csv filess
            
        Args: 
            file_path (str):    path to the csv file 
            
        Returns:
            ret_status (Ret):   the exit status of the process
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
        
        Args: 
            jira (jira obj):    jira obj for restAPi connection with server
            
        Returns:
            ret_status (Ret):   the exit status of the process
        """
        ret_status = Ret.RET_OK

        write_dictionary = self._create_write_dictionary()

        try:
            issue_key = jira.create_issue(fields=write_dictionary).key

        except ex.JIRAError as e:
            print(e)
            ret_status = Ret.RET_ERROR_CREATING_TICKET_FAILED

        if ret_status == Ret.RET_OK:
            print(f"your ticket has been imported with key: \n{issue_key}")

        return ret_status


    def _process_issue(self):
        """store all data in the self._issue member 
           to the issue_dictionary of this Instance
        """
        self._issue_dictionary['key'] = self._issue.key
        self._issue_dictionary['project_key'] = self._issue.fields.project.key

        self._issue_dictionary['summary'] = self._issue.fields.summary

        self._issue_dictionary['description'] = self._issue.fields.description

        if self._issue.fields.issuetype is not None:
            self._issue_dictionary['issuetype'] = self._issue.fields.issuetype.id

        if self._issue.fields.priority is not None:
            self._issue_dictionary['priority'] = self._issue.fields.priority.id

        self._issue_dictionary['duedate'] = self._issue.fields.duedate

        if self._issue.fields.assignee is not None:
            self._issue_dictionary['assignee'] = self._issue.fields.assignee.name

        if self._issue.fields.creator is not None:
            self._issue_dictionary['creator'] = self._issue.fields.creator.displayName

        self._issue_dictionary['creation_date'] = self._issue.fields.created

        self._issue_dictionary['originalEstimate'] = self._issue.fields.timeoriginalestimate

        self._issue_dictionary['remainingEstimate'] = self._issue.fields.timeestimate

        self._issue_dictionary['environment'] = self._issue.fields.environment

        if self._issue.fields.status is not None:
            self._issue_dictionary['status'] = self._issue.fields.status.name

        for label in self._issue.fields.labels:
            self._issue_dictionary['labels'].append(label)
        for component in self._issue.fields.components:
            self._issue_dictionary['components'].append(component.name)
        for version in self._issue.fields.versions:
            self._issue_dictionary['versions'].append(version.name)
        for solution in self._issue.fields.fixVersions:
            self._issue_dictionary['fixVersions'].append(solution.name)

    def _create_write_dictionary(self):
        """prepare the issue information stored in this Instance
           to a format which the jira REST API can convert to a jira issue
           on the server

        Returns:
            write_dictionary (dict):    contains the issue information
        """

        write_dictonary = {}
        time_tracking = {}

        for field in _const.ISSUE_FIELDS:

            if field in _const.EXCLUDED_FIELDS:
                continue

            if self._issue_dictionary[field] is not None or self._issue_dictionary[field] == []:

                if field == 'project_key':
                    write_dictonary['project'] = {"key" : self._issue_dictionary['project_key']}

                elif field == 'issuetype':
                    write_dictonary["issuetype"] = \
                        _const.ISSUE_TYPES[self._issue_dictionary['issuetype']]

                elif field == 'priority':
                    write_dictonary['priority'] = \
                        {"id" : self._issue_dictionary['priority']}

                elif field == 'assignee':
                    write_dictonary['assignee'] = {"name" : self._issue_dictionary['assignee']}

                elif field in ['originalEstimate', 'remainingEstimate']:
                    time_tracking[field] = self._issue_dictionary[field]

                elif field in ['components', 'versions', 'fixVersions']:
                    items = []
                    for item in self._issue_dictionary[field]:
                        items.append({ "name" : item})
                    write_dictonary[field] = items

                else:
                    write_dictonary[field] = self._issue_dictionary[field]

        write_dictonary["timetracking"] = time_tracking

        return write_dictonary
