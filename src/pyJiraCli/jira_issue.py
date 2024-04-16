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
import os
import json
import csv

import jira_server as server
from retval import Ret
################################################################################
# Variables
################################################################################
# all available issue fields
ISSUE_FIELDS = [
            'issue_key',              
            'project_key',            
            'summary',                
            'description',            
            'issuetype',              
            'priority',               
            'duedate',                
            'assignee',               
            'creator',
            'creation_date',            
            'timeestimatedtotal',     
            'timeestimatedremaining', 
            'environment',            
            'status',                 
            'labels',                 
            'components',             
            'versions',               
            'solutions'
        ]

# all fields that can hold mutliple values
LIST_FIELDS = [
            'labels',                 
            'components',             
            'versions',               
            'solutions'
        ]

# fields excluded when creating issues from files
EXCLUDED_FIELDS = [
            'creator',
            'creation_date',
            'issue_key',
            'status'
        ]
################################################################################
# Classes
################################################################################
class JiraIssue:
    """Class contains all jira ticket information"""

    def __init__(self) -> None:
        self._issue_dict = {}

        for field in ISSUE_FIELDS:
            if field in LIST_FIELDS:
                self._issue_dict[field] = []
            else:
                self._issue_dict[field] = None

    def get_key(self):
        """return the issue key of current issue"""
        return self._issue_dict['issue_key']

    def export_issue(self, jira, issue):
        """export issue from jira server"""

        try:
            issue = jira.issue(issue)

        except Exception as e:
            print(e)
            return Ret.RET_ERROR_ISSUE_NOT_FOUND

        self._issue_dict['issue_key'] = issue.key
        self._issue_dict['project_key'] = issue.fields.project.key
        self._issue_dict['summary'] = issue.fields.summary
        self._issue_dict['description'] = issue.fields.description
        self._issue_dict['issuetype'] = issue.fields.issuetype.id
        self._issue_dict['priority'] = issue.fields.priority.id
        self._issue_dict['duedate'] = issue.fields.duedate
        self._issue_dict['assignee'] = issue.fields.assignee.displayName
        self._issue_dict['creator'] = issue.fields.creator.displayName
        self._issue_dict['creation_date'] = issue.fields.creator.displayName
        self._issue_dict['timeestimatedtotal'] = issue.fields.timeoriginalestimate
        self._issue_dict['timeestimatedremaining'] = issue.fields.timeestimate
        self._issue_dict['environment'] = issue.fields.environment
        self._issue_dict['status'] = issue.fields.status.name
        
        for label in issue.fields.labels:
            self._issue_dict['labels'].append(label)
        for component in issue.fields.components:
            self._issue_dict['components'].append(component.name)
        for version in issue.fields.versions:
            self._issue_dict['versions'].append(version.name)
        for solution in issue.fields.fixVersions:
            self._issue_dict['solutions'].append(solution.name)
        
        return Ret.RET_OK

    def import_issue(self, dictonary):
        """"import issue from issue obj"""
        
        # get issue information from json or csv file
        for field in ISSUE_FIELDS:
            if field in dictonary:
                if field in LIST_FIELDS:
                    for item in dictonary[field]:
                        self._issue_dict[field].append(item)
                else:
                    self._issue_dict[field] = dictonary[field]
            
    def print_issue(self):
        """"print issue information containend in class instance"""

    def create_json(self, file_path):
        """"write issue information in class instance to json file"""

        # serialize json object
        json_object = json.dumps(self._issue_dict, indent=4)

        try:
            with open(file_path, "w", encoding='utf-8') as outfile:
                outfile.write(json_object)
        
        except Exception as e:

            # print exception
            print(e)
            return Ret.RET_ERROR_FILE_OPEN_FAILED

        return Ret.RET_OK
    
    def create_csv(self, file_path):
        """"write issue information in class instance to csv file"""
        
        try:
            with open(file_path, "w", encoding='utf-8') as outfile:
                csv_writer = csv.DictWriter(outfile, fieldnames=ISSUE_FIELDS)
                
                csv_writer.writeheader()
                csv_writer.writerow(self._issue_dict)
        
        except Exception as e:
            # print exception
            print(e)
            return Ret.RET_ERROR_FILE_OPEN_FAILED


    def create_ticket(self, jira):
        """create jira issue with information from class instance"""

        write_dictonary = {}

        for field in ISSUE_FIELDS:
            if self._issue_dict[field] is not None or self._issue_dict[field] == []:
                match field:
                    case 'project':
                        write_dictonary['project'] = {"key" : self._issue_dict['project_key']}

            
            # 'summary'                : self._issue_dict['summary'],
            # 'description'            : self._issue_dict['description'],
            # 'issuetype'              : {'id' : self._issue_dict['issuetype']},
            # 'priority'               : {'id' : self._issue_dict['priority']},
            # 'assignee'               : {'displayName' : self._issue_dict['assignee']},          
            # 'timeestimatedtotal'     : self._issue_dict['timeestimatedtotal'], 
            # 'timeestimatedremaining' : self._issue_dict['timeestimatedremaining'],  
            # 'environment'            : self._issue_dict['environment'],
            # 'labels'                 : self._issue_dict['labels'],
            # 'components'             : self._issue_dict['components'],
            # 'versions'               : self._issue_dict['versions'],
            # 'solutions'              : self._issue_dict['solutions']
        
        
        try:
            jira.create_issue(fields=write_dictonary)

        except Exception as e:
            print(e)
            return Ret.RET_ERROR_CREATING_TICKET_FAILED

        return Ret.RET_OK
################################################################################
# Functions
################################################################################
