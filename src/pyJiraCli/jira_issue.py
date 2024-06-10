"""Jira issue Class.
   this Class contains all issue information
   provides functions to load issues from JSON and csv files or 
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

from pyJiraCli.ret import Ret
from pyJiraCli.file_handler import FileHandler as File
from pyJiraCli import issue_constants as _const
################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################
class JiraIssue:
    """ Class contains all jira ticket information
        and methods to convert between JSON/csv files
        and server issues.
    """
    def __init__(self) -> None:
        self._file_h = File()
        self._issue_dictionary = {}
        self._issue = None

    def get_key(self) -> str:
        """ Return the issue key of current issue.
        
        Returns:
            key (str):  The current issue key or None.
        """
        key = None

        if self._issue is not None:
            key = self._issue.key

        return key

    def export_issue(self, jira, issue:str) -> Ret.CODE:
        """ Load the issue from the jira server
            and store its information in the instance
            of the class. 
            
        Args:
            jira (obj):    The jira obj for restAPi connection with the server.
            issue (str):   The issue key in string format.
            
        Returns:
            Ret.CODE:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
        """
        ret_status = Ret.CODE.RET_OK

        try:
            self._issue = jira.issue(issue)

        except ex.JIRAError as e:
            print(e.text)
            ret_status = Ret.CODE.RET_ERROR_ISSUE_NOT_FOUND

        return ret_status

    def import_issue(self, dictionary) -> None:
        """ Import issue from a dictionary.

            Store all values which have a key 
            in the instances issue_dict to the
            class instance. 
        
        Args:
            dictionary (dict): A python dictionary conatining jira issue info.
        """

        # get issue information from JSON or csv file
        for field in dictionary:
            if field in _const.ISSUE_FIELDS:
                self._issue_dictionary[field] = dictionary[field]

    def print_issue(self) -> None:
        """ Print issue information contained
            in class instance to the command line.
        """
        print_data = json.dumps(self._issue.raw, indent=4)
        print(print_data)

    def create_json(self, file_path):
        """ write issue information in class instance to a JSON file
            
        Args: 
            file_path (str):    The path to the JSON file. 
            
        Returns:
            Ret.CODE:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
        """
        ret_status = Ret.CODE.RET_OK

        # serialize JSON object
        json_object = json.dumps(self._issue.raw, indent=4)

        ret_status = self._file_h.set_filepath(file_path)

        if ret_status == Ret.CODE.RET_OK:
            ret_status = self._file_h.write_file(json_object)

        self._file_h.close_file()

        return ret_status

    def create_csv(self, file_path) -> Ret.CODE:
        """ Write issue information in class instance to a csv file.
            
        Args: 
            file_path (str):    The path to the csv file. 
            
        Returns:
            Ret.CODE:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
        """
        ret_status = Ret.CODE.RET_OK

        ret_status = self._file_h.set_filepath(file_path)

        if ret_status == Ret.CODE.RET_OK:
            ret_status = self._file_h.open_file(file_mode='w')

        if ret_status == Ret.CODE.RET_OK:
            csv_writer = csv.DictWriter(self._file_h.get_file(),
                                        delimiter=';',
                                        fieldnames=_const.ISSUE_FIELDS)

            csv_writer.writeheader()
            csv_writer.writerow(self._issue_dictionary)

        self._file_h.close_file()

        return ret_status

    def create_ticket(self, jira) -> Ret.CODE:
        """ Create jira issue on the server with information from class instance.
        
        Args: 
            jira (obj):    The jira obj for restAPi connection with server.
            
        Returns:
            Ret.CODE:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
        """
        issue_key = None

        write_dictionary = self._create_write_dictionary()

        try:
            issue_key = jira.create_issue(fields=write_dictionary).key

        except ex.JIRAError as e:
            print(e.text)

        return issue_key

    def _create_write_dictionary(self) -> dict:
        """ Prepare the issue information stored in this Instance,
            to a format which the jira REST API can convert to a jira issue
            on the server.

        Returns:
            write_dictionary (dict):    A dictionary containng the issue information in a
                                        format which can be written to the jira server.
        """

        write_dictonary = {}
        time_tracking = {}

        for field in _const.ISSUE_FIELDS:

            if field in _const.EXCLUDED_FIELDS:
                continue

            if self._issue_dictionary[field] is not None or \
               self._issue_dictionary[field] == []:

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
