"""crpyto module for information file handling.
   provides function to encrypt and decrypt user or server information
   to and from files"""
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

from retval import Ret
################################################################################
# Variables
################################################################################
SERVER_INFO_FILE_LOCATION = ".\\.logindata\\.server.txt"
USER_INFO_FILE_LOCATION   = ".\\.logindata\\.user.txt"
################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################
def encrypt_user_information(user, pw):
    """"encrypt userinformation to file"""
    json_object = json.dumps({'user' : user,'pw' : pw}, indent=4)
   
    try:
        with open(USER_INFO_FILE_LOCATION, "w", encoding='utf-8') as outfile:
            outfile.write(json_object)
        
    except Exception as e:
        # print exception
        print(e)
        return Ret.RET_ERROR_FILE_OPEN_FAILED

    return Ret.RET_OK

def decrypt_user_information():
    """"decrypt and return userinformation from file"""
    user = None
    pw = None

    if os.path.exists(USER_INFO_FILE_LOCATION):
        try:
            with open(USER_INFO_FILE_LOCATION, 'r', encoding='utf-8') as file:
                data = json.load(file)
                user = data['user']
                pw = data['pw']
    
        except Exception as e:
            # print exception
            print(e)
            return user, pw, Ret.RET_ERROR_FILE_OPEN_FAILED
    else:
        return user, pw, Ret.RET_ERROR_LOGIN_FILE_MISSING
    
    return user, pw, Ret.RET_OK

def encrypt_server_information(server_url):
    """"encrypt server information to file"""
    json_object = json.dumps({'url' : server_url}, indent=4)
   
    try:
        with open(SERVER_INFO_FILE_LOCATION, "w", encoding='utf-8') as outfile:
            outfile.write(json_object)
        
    except Exception as e:
        # print exception
        print(e)
        return Ret.RET_ERROR_FILE_OPEN_FAILED

    return Ret.RET_OK

def decrypt_server_information():
    """"decrypt and return server information from file"""
    
    server = None
    if os.path.exists(SERVER_INFO_FILE_LOCATION):
        try:
            with open(SERVER_INFO_FILE_LOCATION, 'r', encoding='utf-8') as file:
                data = json.load(file)
                server = data['url']
    
        except Exception as e:
            # print exception
            print(e)
            return server, Ret.RET_ERROR_FILE_OPEN_FAILED
    else:
        return server, Ret.RET_ERROR_LOGIN_FILE_MISSING
    
    return server, Ret.RET_OK


def delete_user_information():
    """delete user information file"""
    if os.path.exists(USER_INFO_FILE_LOCATION):
        os.remove(USER_INFO_FILE_LOCATION)

def delete_server_information():
    """delete server information file"""
    if os.path.exists(SERVER_INFO_FILE_LOCATION):
        os.remove(SERVER_INFO_FILE_LOCATION)