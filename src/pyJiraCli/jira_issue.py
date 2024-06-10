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

from pyJiraCli.ret import Ret
from pyJiraCli.file_handler import FileHandler as File
from pyJiraCli import issue_constants as _const
################################################################################
# Variables
################################################################################
KEY_FIELD_COL_WIDTH = 25
DATA_FIELD_COL_WIDTH = 100
################################################################################
# Classes
################################################################################
class JiraIssue:
    """ Class contains all jira ticket information
        and methods to convert between json/csv files
        and server issues.
    """
    def __init__(self) -> None:
        self._file_h = File()
        self._issue_dictionary = {}
        self._issue = None

        for field in _const.ISSUE_FIELDS:
            if field in _const.LIST_FIELDS:
                self._issue_dictionary[field] = []
            else:
                self._issue_dictionary[field] = None

    def get_key(self) -> str:
        """ Return the issue key of current issue.
        
        Returns:
            key (str):  The current issue key or None.
        """
        key = None

        if 'key' in self._issue_dictionary:
            key = self._issue_dictionary['key']

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

        if ret_status == Ret.CODE.RET_OK:
            self.process_issue()

        return ret_status

    def import_issue(self, dictionary) -> None:
        """ Import issue from a dictionary.

            Store all values which have a key 
            in the instances issue_dict to the
            class instance. 
        
        Args:
            dictionary (dict): A python dictionary conatining jira issue info.
        """

        # get issue information from json or csv file
        for field in dictionary:
            if field in _const.ISSUE_FIELDS:
                self._issue_dictionary[field] = dictionary[field]

    def print_issue(self) -> None:
        """ Print issue information contained
            in class instance to the command line.
        """
        for field_name, field_data in self._issue_dictionary.items():

            print(f"{field_name:<{KEY_FIELD_COL_WIDTH}}", end="")

            data_str = str(field_data)
            if len(data_str) <= DATA_FIELD_COL_WIDTH:
                print(f"{data_str:<{DATA_FIELD_COL_WIDTH}}")
            else:
                self._print_long_data_line(data_str)

    def _print_long_data_line(self, data_str:str) -> None:
        """ This functio handles long value lines,
            when printing ticket information.
            The line will be split into separate parts
            and each part will printed in a new line
            aligned with the others.

        Args:
            data_str (str): The text that shall be printed to the screen.
        """
        printable_lines = []

        lines = data_str.split('\n')  # Split description into lines
        print_first_line = True

        for line in lines:
            if len(line) > DATA_FIELD_COL_WIDTH:
                printable_lines = printable_lines + self._split_line(line)

            elif len(line) == 0:
                pass

            else:
                printable_lines.append(line)

        for line in printable_lines:
            if print_first_line:
                print(line)
                print_first_line = False
            else:
                if line[0] == ' ':
                    line = line[1:]

                print((" " * KEY_FIELD_COL_WIDTH) + line)

    def _split_line(self, line:str) -> list:
        """ If a line is still too long after being split into
            paragraphs, it'll further be split into sentences
            or words when necessary.

        Args:
            line (str): The paragraph that is still too long.

        Returns:
            list: A list of printable lines.
        """
        printable_lines = []
        split_lines = line.split('. ')

        new_line = ""

        for split_line in split_lines:

            if len(split_line) > DATA_FIELD_COL_WIDTH:
                words_in_line = split_line.split(' ')

                for word in words_in_line:

                    if (len(word) + len(new_line) + 1) <= DATA_FIELD_COL_WIDTH:
                        new_line += word + " "
                    else:
                        printable_lines.append(new_line)
                        new_line = ""

                if len(new_line) > 0:
                    printable_lines.append(new_line)
            else:
                if split_line[-1:] != '.':
                    split_line = split_line + '.'

                printable_lines.append(split_line)

        return printable_lines

    def create_json(self, file_path):
        """ write issue information in class instance to a json file
            
        Args: 
            file_path (str):    The path to the json file. 
            
        Returns:
            Ret.CODE:   Returns Ret.CODE.RET_OK if successful or else the corresponding error code.
        """
        ret_status = Ret.CODE.RET_OK

        # serialize json object
        json_object = json.dumps(self._issue_dictionary, indent=4)

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

    def process_issue(self) -> None:
        """ Process data in the self._issue member and
            transfer it to the issue_dictionary of this Instance.
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

        if self._issue.fields.timeoriginalestimate is not None:
            self._issue_dictionary['originalEstimate'] = \
                self._issue.fields.timeoriginalestimate // 3600

        if self._issue.fields.timeestimate is not None:
            self._issue_dictionary['remainingEstimate'] = \
                self._issue.fields.timeestimate // 3600

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
