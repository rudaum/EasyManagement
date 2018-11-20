#!/usr/bin/python
"""
-Purpose:
    To retrieve information from Ansible Clients and store
    the data in a Mysql Database.
-Author:
    Rudolf Wolter
-Contact for questions and/or comments:
    rudolf.wolter@kuehne-nagel.com
-Parameters:
    None
-Version Releases and modifications.
    0.1 - 10 Sep 2018: Initial Release
"""
### START OF MODULE IMPORTS ###
# --------------------------------------------------------------- #
import os
import sys
from datetime import datetime
path = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('{0}/../../'.format(path))
from subprocess import call
from main.lib.settings import PLAYBOOKBIN, PBDIR, SAFESERVER, NULLSTR
from main.lib.dblib import mk_dbenv, User

# --------------------------------------------------------------- #
### END OF MODULE IMPORTS ###

### START OF GLOBAL VARIABLES DECLARATION
# --------------------------------------------------------------- #
## General Vars
ARGS = sys.argv
NARGS = len(ARGS[1:])
PBOUTPUTDIR = PBDIR + "output/lsuser/"
# --------------------------------------------------------------- #
### END OF GLOBAL VARIABLES DECLARATION ###

### START OF FUNCTIONS DECLARATION ###
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
### END OF FUNCTIONS DECLARATION

### START OF CLASS DEFINITIONS
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
### END OF CLASS DEFINITIONS

### START OF MAIN PROGRAM
"""
Purpose:
    Executes the Ansible Playbook responsible for retrieving User information from Ansible clients.
    Stores the information as User Objects hosted by the a OrderedDict variable for later DB trasactions

Parameters:
    targ_hosts: The Ansibles Clients that will have their information collected
"""

# If no Target Host are give, use a SAFE as security measure
targ_hosts = ARGS[1] if NARGS > 0 else SAFESERVER
targ_hosts = targ_hosts

# Creating the Empty Tables in the Database f it doesn't exist yet
mk_dbenv()

# Querying servers from the Database and storing the results in a Ordered Dict
ordered_dict = User().query_all()

# setting the Ansible Command
ans_cmd = [PLAYBOOKBIN, PBDIR + "lsuser.yml", "-l", targ_hosts]

# Calling Ansible process
print ('Trying to retrieve Users info from Ansible Clients ...')
try:
    call(ans_cmd)
except OSError as err_msg:
    print('Could not execute "{}":\n{}'.format(ans_cmd, err_msg))
print ('Success! Retrieved Users info from Ansible Clients')

# Creating Server Classes from the Files generated from the Ansible Playbook
for filename in os.listdir(PBOUTPUTDIR):
    if filename.endswith(".pb"):
        host = os.path.basename(filename).replace(".pb", "")
        _file = open(os.path.join(PBOUTPUTDIR, filename))
        userlist = eval('[' + _file.readline().replace(', "-NEXT-", ', '],[').replace(', "-NEXT-"]', ']') + ']')
        print ('Parsing/Persisting Users for {} ...'.format(host))
        for user in userlist:
            username = user[0].split('=')[1]
            dictidx = username + '_' + host
            if dictidx not in ordered_dict.keys():
                ordered_dict[dictidx] = User()

            ordered_dict[dictidx].user_server = dictidx
            ordered_dict[dictidx].user_name = username
            ordered_dict[dictidx].server_name = host
            for attribute in user[1:]:
                attr = attribute.split('=')[0]
                #                               Some Attributes are null
                value = attribute.split('=')[1] if len(attribute.split('=')[1]) > 0 else NULLSTR
                if attr == "id":
                    ordered_dict[dictidx].user_id = value
                elif attr == "pgrp":
                    ordered_dict[dictidx].primary_group = value
                elif attr == "groups":
                    ordered_dict[dictidx].groups = value
                elif attr == "home":
                    ordered_dict[dictidx].home = value
                elif attr == "gecos":
                    ordered_dict[dictidx].gecos = value
                elif attr == "time_last_login":
                    if value == NULLSTR:
                        datestamp = datetime.utcfromtimestamp(float(0)).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        datestamp = datetime.utcfromtimestamp(float(value)).strftime('%Y-%m-%d %H:%M:%S')
                    ordered_dict[dictidx].time_last_login = datestamp
                elif attr == "unsuccessful_login_count":
                    ordered_dict[dictidx].unsuccessful_login_count = value
                elif attr == "maxage":
                    ordered_dict[dictidx].maxage = value
                elif attr == "shell":
                    ordered_dict[dictidx].shell = value
                elif attr == "umask":
                    ordered_dict[dictidx].umask = value
                elif attr == "fsize":
                    ordered_dict[dictidx].fsize = value
                elif attr == "cpu":
                    ordered_dict[dictidx].cpu = value
                elif attr == "data":
                    ordered_dict[dictidx].data = value
                elif attr == "stack":
                    ordered_dict[dictidx].stack = value
                elif attr == "core":
                    ordered_dict[dictidx].core = value
                elif attr == "rss":
                    ordered_dict[dictidx].rss = value
                elif attr == "nofiles":
                    ordered_dict[dictidx].nofiles = value
                elif attr == "login":
                    ordered_dict[dictidx].login = value
                elif attr == "su":
                    ordered_dict[dictidx].su = value
                elif attr == "rlogin":
                    ordered_dict[dictidx].rlogin = value
                elif attr == "daemon":
                    ordered_dict[dictidx].daemon = value
                elif attr == "admin":
                    ordered_dict[dictidx].admin = value
                elif attr == "sugroups":
                    ordered_dict[dictidx].sugroups = value
                elif attr == "admgroups":
                    ordered_dict[dictidx].admgroups = value
                elif attr == "tpath":
                    ordered_dict[dictidx].tpath = value
                elif attr == "ttys":
                    ordered_dict[dictidx].ttys = value
                elif attr == "expires":
                    ordered_dict[dictidx].expires = value
                elif attr == "auth1":
                    ordered_dict[dictidx].auth1 = value
                elif attr == "auth2":
                    ordered_dict[dictidx].auth2 = value
                elif attr == "registry":
                    ordered_dict[dictidx].registry = value
                elif attr == "SYSTEM":
                    ordered_dict[dictidx].system = value
                elif attr == "logintimes":
                    ordered_dict[dictidx].logintimes = value
                elif attr == "loginretries":
                    ordered_dict[dictidx].loginretries = value
                elif attr == "pwdwarntime":
                    ordered_dict[dictidx].pwdwarntime = value
                elif attr == "account_locked":
                    ordered_dict[dictidx].account_locked = value
                elif attr == "minage":
                    ordered_dict[dictidx].minage = value
                elif attr == "maxexpired":
                    ordered_dict[dictidx].maxexpired = value
                elif attr == "minalpha":
                    ordered_dict[dictidx].minalpha = value
                elif attr == "minother":
                    ordered_dict[dictidx].minother = value
                elif attr == "mindiff":
                    ordered_dict[dictidx].mindiff = value
                elif attr == "maxrepeats":
                    ordered_dict[dictidx].maxrepeats = value
                elif attr == "minlen":
                    ordered_dict[dictidx].minlen = value
                elif attr == "histexpire":
                    ordered_dict[dictidx].histexpire = value
                elif attr == "histsize":
                    ordered_dict[dictidx].histsize = value
                elif attr == "pwdchecks":
                    ordered_dict[dictidx].pwdchecks = value
                elif attr == "dictionlist":
                    ordered_dict[dictidx].dictionlist = value
                elif attr == "default_roles":
                    ordered_dict[dictidx].default_roles = value
                elif attr == "roles":
                    ordered_dict[dictidx].roles = value

            # Persisting the User Object into the database
            ordered_dict[dictidx].update()
        print ('Success! Parsed/Persisted Users for {}'.format(host))
### END OF MAIN PROGRAM
