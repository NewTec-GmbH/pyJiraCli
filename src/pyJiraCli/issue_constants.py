"""Contains constant values"""

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

################################################################################
# Variables
################################################################################
ISSUE_TYPES = {
    '1' : 'Bug',
    '2' : 'Neue Funktion',
    '3' : 'Aufgabe',
    '4' : 'Story',
    '5' : 'Epos',
    '6' : 'ToDo',
    '7' : 'Änderungsantrag (Dev)',
    '8' : 'QMeldung'
}

ISSUE_PRIORITIES = {
    '1' : 'Blocker',
    '2' : 'Kritisch',
    '3' : 'Major (Default)',
    '4' : 'Geringfügig',
    '5' : 'UNwesentlich'
}

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

################################################################################
# Functions
################################################################################
