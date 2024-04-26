""" Command to search for Jira tickets on the provided server.
    Searches for tickets by filter or search str provided via the command line 
    and prints all found tickets to command line. """

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
from pyJiraCli.ret import Ret
################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################
def register(subparser):
    """ Register subparser commands for the login module.
        
    Args:
        subparser (obj):   the command subparser provided via __main__.py
        
    Returns:
        obj:    the commmand parser of this module
    """
    # subparser for the 'search' command
    sb_search = subparser.add_parser('search',
                                      help="search for jira issues \
                                            with specified filter string")

    sb_search.add_argument('filter',
                            type=str,
                            help="filter string according to \
                                  which issue are to be searched")

    return sb_search

def execute(args) -> Ret:
    """ Execute the search command function.
    
    Args: 
        args (obj): the command line arguments
        
    Returns:
        Ret:   Ret.RET_OK if succesfull, corresponding error code if not
    """
    return _cmd_search(args.filter, args.user, args.pw)

def _cmd_search(filter_str:str, user:str, pw:str) -> Ret:
    """ Search tickets with a provided filter or search string.
    
    Args:
        filter_str (str):   string containing the search parameters
        user (str):         username for login
        pw (str)            password for login
    
    Returns:
        Ret:   Ret.RET_OK if succesfull, corresponding error code if not
    """
    print(f"searching for issues with filter {filter_str, user, pw}")

    return Ret.RET_OK
