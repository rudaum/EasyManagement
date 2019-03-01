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
from collections import OrderedDict
path = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('{0}/../../'.format(path))
from subprocess import call
from main.lib.settings import PLAYBOOKBIN, PBDIR, SAFESERVER, NULLSTR
from main.lib.dblib import mk_dbenv, User, UserChanges
# --------------------------------------------------------------- #
### END OF MODULE IMPORTS ###

### START OF GLOBAL VARIABLES DECLARATION
# --------------------------------------------------------------- #
## General Vars
ARGS = sys.argv
NARGS = len(ARGS[1:])
PBOUTPUTDIR = PBDIR + "output/lsuser/"
IGNORED_ATTR = ["unsuccessful_login_count", "time_last_login"]
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
users_query = User().query_all()
orddict_users_from_db = OrderedDict()
for entry in users_query:
    orddict_users_from_db[entry.user_server] = entry

# setting the Ansible Command
ans_cmd = [PLAYBOOKBIN, PBDIR + "lsuser.yml", "-l", targ_hosts]

# Calling Ansible process
print ('Trying to retrieve Users info from Ansible Clients ...')
try:
    call(ans_cmd)
    print ('Success! Retrieved Users info from Ansible Clients')
except OSError as err_msg:
    print('Could not execute "{}":\n{}'.format(ans_cmd, err_msg))


# Creating Server Classes from the Files generated from the Ansible Playbook
for filename in os.listdir(PBOUTPUTDIR):
    if filename.endswith(".pb"):
        host = os.path.basename(filename).replace(".pb", "")
        _file = open(os.path.join(PBOUTPUTDIR, filename))
        # Transforming Ansible result file into an Array of values.
        userlist = eval('[' + _file.readline().replace(', "-NEXT-", ', '],[').replace(', "-NEXT-"]', ']') + ']')

        print ('Parsing/Persisting Users for {} ...'.format(host))
        checked_users = []  # Contains Users that still exists and were not removed since last check
        changes_dict = []
        # Getting the current timestamp to be used as "Detected on" value.
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for user in userlist:
            newuser = False
            username = user[0].split('=')[1]
            dictidx = username + '_' + host
            if dictidx not in orddict_users_from_db.keys():
                orddict_users_from_db[dictidx] = User()
                newuser = True
                changes_dict.append([username, host, 'user', 'not-present', 'present', now])

            orddict_users_from_db[dictidx].user_server = dictidx
            orddict_users_from_db[dictidx].user_name = username
            orddict_users_from_db[dictidx].server_name = host
            checked_users.append(dictidx)
            for attribute in user[1:]:
                attr = attribute.split('=')[0]
                #                               Some Attributes are null
                value = attribute.split('=')[1] if len(attribute.split('=')[1]) > 0 else NULLSTR

                # transforming 'id' and pgrp attrs in equivalent name for the DB;l
                tmpattr = 'user_id' if attr == 'id' else attr
                tmpattr = 'primary_group' if tmpattr == 'pgrp' else tmpattr
                try:
                    # if it is not an ignorable attribute and it is not a new user, compare old and new values
                    if tmpattr not in IGNORED_ATTR and not newuser:
                        db_value = User().query_by('user_server', dictidx)[0].get_column_value(tmpattr)
                        if str(db_value) != str(value):
                            changes_dict.append([username, host, attr, db_value, value, now])
                except AttributeError:
                    continue

                if attr == "id":
                    orddict_users_from_db[dictidx].user_id = value
                elif attr == "pgrp":
                    orddict_users_from_db[dictidx].primary_group = value
                elif attr == "groups":
                    orddict_users_from_db[dictidx].groups = value
                elif attr == "home":
                    orddict_users_from_db[dictidx].home = value
                elif attr == "gecos":
                    orddict_users_from_db[dictidx].gecos = value
                elif attr == "time_last_login":
                    if value == NULLSTR:
                        datestamp = datetime.utcfromtimestamp(float(0)).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        datestamp = datetime.utcfromtimestamp(float(value)).strftime('%Y-%m-%d %H:%M:%S')
                    orddict_users_from_db[dictidx].time_last_login = datestamp
                elif attr == "unsuccessful_login_count":
                    orddict_users_from_db[dictidx].unsuccessful_login_count = value
                elif attr == "maxage":
                    orddict_users_from_db[dictidx].maxage = value
                elif attr == "shell":
                    orddict_users_from_db[dictidx].shell = value
                elif attr == "umask":
                    orddict_users_from_db[dictidx].umask = value
                elif attr == "fsize":
                    orddict_users_from_db[dictidx].fsize = value
                elif attr == "cpu":
                    orddict_users_from_db[dictidx].cpu = value
                elif attr == "data":
                    orddict_users_from_db[dictidx].data = value
                elif attr == "stack":
                    orddict_users_from_db[dictidx].stack = value
                elif attr == "core":
                    orddict_users_from_db[dictidx].core = value
                elif attr == "rss":
                    orddict_users_from_db[dictidx].rss = value
                elif attr == "nofiles":
                    orddict_users_from_db[dictidx].nofiles = value
                elif attr == "login":
                    orddict_users_from_db[dictidx].login = value
                elif attr == "su":
                    orddict_users_from_db[dictidx].su = value
                elif attr == "rlogin":
                    orddict_users_from_db[dictidx].rlogin = value
                elif attr == "daemon":
                    orddict_users_from_db[dictidx].daemon = value
                elif attr == "admin":
                    orddict_users_from_db[dictidx].admin = value
                elif attr == "sugroups":
                    orddict_users_from_db[dictidx].sugroups = value
                elif attr == "admgroups":
                    orddict_users_from_db[dictidx].admgroups = value
                elif attr == "tpath":
                    orddict_users_from_db[dictidx].tpath = value
                elif attr == "ttys":
                    orddict_users_from_db[dictidx].ttys = value
                elif attr == "expires":
                    orddict_users_from_db[dictidx].expires = value
                elif attr == "auth1":
                    orddict_users_from_db[dictidx].auth1 = value
                elif attr == "auth2":
                    orddict_users_from_db[dictidx].auth2 = value
                elif attr == "registry":
                    orddict_users_from_db[dictidx].registry = value
                elif attr == "SYSTEM":
                    orddict_users_from_db[dictidx].system = value
                elif attr == "logintimes":
                    orddict_users_from_db[dictidx].logintimes = value
                elif attr == "loginretries":
                    orddict_users_from_db[dictidx].loginretries = value
                elif attr == "pwdwarntime":
                    orddict_users_from_db[dictidx].pwdwarntime = value
                elif attr == "account_locked":
                    orddict_users_from_db[dictidx].account_locked = value
                elif attr == "minage":
                    orddict_users_from_db[dictidx].minage = value
                elif attr == "maxexpired":
                    orddict_users_from_db[dictidx].maxexpired = value
                elif attr == "minalpha":
                    orddict_users_from_db[dictidx].minalpha = value
                elif attr == "minother":
                    orddict_users_from_db[dictidx].minother = value
                elif attr == "mindiff":
                    orddict_users_from_db[dictidx].mindiff = value
                elif attr == "maxrepeats":
                    orddict_users_from_db[dictidx].maxrepeats = value
                elif attr == "minlen":
                    orddict_users_from_db[dictidx].minlen = value
                elif attr == "histexpire":
                    orddict_users_from_db[dictidx].histexpire = value
                elif attr == "histsize":
                    orddict_users_from_db[dictidx].histsize = value
                elif attr == "pwdchecks":
                    orddict_users_from_db[dictidx].pwdchecks = value
                elif attr == "dictionlist":
                    orddict_users_from_db[dictidx].dictionlist = value
                elif attr == "default_roles":
                    orddict_users_from_db[dictidx].default_roles = value
                elif attr == "roles":
                    orddict_users_from_db[dictidx].roles = value

            # Persisting the User Object into the database
            orddict_users_from_db[dictidx].update()

        print ('Processing the User changes since last run ...')
        # Checking Users  that were deleted
        for user_server in orddict_users_from_db.keys():
            if user_server not in checked_users and host in user_server:
                user_name = user_server.split('_')[0]
                changes_dict.append([user_name, host, 'user', 'present', 'not-present', now])
                orddict_users_from_db[user_server].delete()

        for change in changes_dict:
            ch = UserChanges()
            ch.user_name = change[0]
            ch.server_name = change[1]
            ch.attribute_name = change[2]
            ch.old_value = change[3]
            ch.new_value = change[4]
            ch.detected_on = change[5]
            ch.update()
        print ('Success! Parsed/Persisted Users for {}'.format(host))
### END OF MAIN PROGRAM
