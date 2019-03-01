#!/usr/bin/python
"""
- Purpose:
    To retrieve information from Ansible Clients and store
    the data in a Mysql Database.
- Author:
    Rudolf Wolter
- Contact for questions and/or comments:
    rudolf.wolter@kuehne-nagel.com
- Parameters:
    None
- Version Releases and modifications.
    0.1 - 10 Sep 2018: Initial Release
"""

### START OF MODULE IMPORTS
# --------------------------------------------------------------- #
import os
import sys
from collections import OrderedDict
from datetime import datetime
path = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(path + '/../../')
from subprocess import call
from main.lib.settings import PLAYBOOKBIN, PBDIR, SAFESERVER, NULLSTR
from main.lib.dblib import mk_dbenv, RPM, RPMChanges

# --------------------------------------------------------------- #
### END OF MODULE IMPORTS

### START OF GLOBAL VARIABLES DECLARATION
# --------------------------------------------------------------- #
## General Vars
ARGS = sys.argv
NARGS = len(ARGS[1:])
PBOUTPUTDIR = PBDIR + "output/lsrpm/"
# --------------------------------------------------------------- #
### END OF GLOBAL VARIABLES DECLARATION

### START OF FUNCTIONS DECLARATION
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
    Executes the Ansible Playbook responsible for retrieving RPM PAckages information from Ansible clients.
    Stores the information as RPM Objects hosted by the a OrderedDict variable for later DB transactions

Parameters:
    targ_hosts: The Ansibles Clients that will have their information collected
"""

# If no Target Host are give, use a SAFE as security measure
targ_hosts = ARGS[1] if NARGS > 0 else SAFESERVER
targ_hosts = targ_hosts

# Creating the Empty Tables in the Database f it doesn't exist yet
mk_dbenv()

# Querying servers from the Database and storing the results in a Ordered Dict
rpm_query = RPM().query_all()
orddict_rpms_from_db = OrderedDict()
for entry in rpm_query:
    orddict_rpms_from_db[entry.rpm_server] = entry

# setting the Ansible Command
ans_cmd = [PLAYBOOKBIN, PBDIR + "lsrpm.yml", "-l", targ_hosts]

# Calling Ansible process
print ('Trying to retrieve RPM info from Ansible Clients ...')
try:
    call(ans_cmd)
    print ('Success! Retrieved RPM info from Ansible Clients')
except OSError as err_msg:
    print('Could not execute "{}":\n{}'.format(ans_cmd, err_msg))

# Creating RPM Classes from the Files generated from the Ansible Playbook
for filename in os.listdir(PBOUTPUTDIR):
    if filename.endswith(".pb"):
        host = os.path.basename(filename).replace(".pb", "")
        _file = open(os.path.join(PBOUTPUTDIR, filename))
        # Transforming Ansible result file into an Array of values.
        rpm_list = eval('[' + _file.readline().replace(', "-NEXT-", ', '],[').replace(', "-NEXT-"]', ']') + ']')
        print ('Parsing/Persisting Server: {} ...'.format(host))
        changes_dict = []
        checked_rpms = []  # Contains RPM that still exists and were not uninstalled since last check
        # Getting the current timestamp to be used as "Detected on" value.
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Looping over the RPM results queried from the Ansible to build a "changes" dictionary
        for rpm in rpm_list:
            newrpm = False
            rpm_name = rpm[0].split('=')[1]
            dictidx = rpm_name + '_' + host
            if dictidx not in orddict_rpms_from_db.keys():
                orddict_rpms_from_db[dictidx] = RPM()
                newrpm = True
                changes_dict.append([rpm_name, host, 'rpm', 'installed', 'not-installed', now])
            orddict_rpms_from_db[dictidx].rpm_server = dictidx
            orddict_rpms_from_db[dictidx].rpm = rpm_name
            orddict_rpms_from_db[dictidx].server_name = host
            checked_rpms.append(dictidx)

            for attribute in rpm[1:]:
                attr = attribute.split('=')[0]
                value = attribute.split('=')[1] if len(attribute.split('=')[1]) > 0 else NULLSTR  # Skipping empty attr.
                if attr == "Version":
                    if orddict_rpms_from_db[dictidx].version != value and not newrpm:
                        changes_dict.append([rpm_name, host, 'Version', value, orddict_rpms_from_db[dictidx].version, now])
                    orddict_rpms_from_db[dictidx].version = value
                elif attr == "Release":
                    if orddict_rpms_from_db[dictidx].release != value and not newrpm:
                        changes_dict.append(
                            [rpm_name, host, 'Release', value, orddict_rpms_from_db[dictidx].release, now])
                    orddict_rpms_from_db[dictidx].release = value
                elif attr == "Install Date":
                    d8 = value.split()
                    if len(d8) > 5:
                        datestamp = datetime.strptime('{} {} {} {}'.format(d8[2], d8[1], d8[5], d8[3]),
                                                      '%d %b %Y %H:%M:%S')
                    else:
                        datestamp = datetime.strptime('{} {} {} {}'.format(d8[2], d8[1], d8[4], d8[3]),
                                                      '%d %b %Y %H:%M:%S')
                    if orddict_rpms_from_db[dictidx].install_date != datestamp and not newrpm:
                        changes_dict.append([rpm_name, host, 'Install Date', datestamp,
                                             orddict_rpms_from_db[dictidx].install_date, now])
                    orddict_rpms_from_db[dictidx].install_date = datestamp
                elif attr == "License":
                    orddict_rpms_from_db[dictidx].license = value
                elif attr == "Build Date":
                    orddict_rpms_from_db[dictidx].build_date = value
                elif attr == "Build Host":
                    orddict_rpms_from_db[dictidx].build_host = value
                elif attr == "Relocations":
                    orddict_rpms_from_db[dictidx].relocations = value

            # Persisting the RPM Object into the database
            orddict_rpms_from_db[dictidx].update()

        print ('Processing the RPM changes since last run ...')
        # Checking Any uninstalled RPM packages
        for rpm_server in orddict_rpms_from_db.keys():
            if rpm_server not in checked_rpms and host in rpm_server:
                rpm_name = rpm_server.split('_')[0]
                changes_dict.append([rpm_name, host, 'rpm', 'not-installed', 'installed', now])
                orddict_rpms_from_db[rpm_server].delete()

        # Persisting the RPM Changes into the database
        for change in changes_dict:
            rpm_changes = RPMChanges()
            rpm_changes.rpm_name = change[0]
            rpm_changes.server_name = change[1]
            rpm_changes.attribute_name = change[2]
            rpm_changes.new_value = change[3]
            rpm_changes.old_value = change[4]
            rpm_changes.detected_on = change[5]
            rpm_changes.update()
        print ('Success! Parsed/Persisted RPMs for {}'.format(host))
### END OF MAIN PROGRAM
