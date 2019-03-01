#!/usr/bin/python
# - Purpose:
#       To retrieve information from Ansible Clients and store
#		the data in a Mysql Database.
# - Author:
#       Rudolf Wolter
# - Contact for questions and/or comments:
#       rudolf.wolter@kuehne-nagel.com
# - Parameters:
#       None
# - Version Releases and modifications.
#       0.1 - 10 Sep 2018: Initial Release

### START OF MODULE IMPORTS
# --------------------------------------------------------------- #
import os
import sys
from datetime import datetime
from collections import OrderedDict
from subprocess import call
path = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(path + '/../../')
from main.lib.dblib import mk_dbenv, Server, ServerChanges
from main.lib.settings import PLAYBOOKBIN, PBDIR, SAFESERVER
# --------------------------------------------------------------- #
### END OF MODULE IMPORTS

### START OF GLOBAL VARIABLES DECLARATION
# --------------------------------------------------------------- #
## General Vars
ARGS = sys.argv
NARGS = len(ARGS[1:])
PBOUTPUTDIR = PBDIR + "output/lsserver/"
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
    Executes the Ansible Playbook responsible for retrieving General Server information from Ansible clients.
    Stores the information in the Server Objects hosted by the HOSTDICT Global variable for later DB transactions

Parameters:
    targ_hosts: The Ansibles Clients that will have their information collected
"""

# If no Target Hosts are given, then use a SAFE host as security measure
targ_hosts = ARGS[1] if NARGS > 0 else SAFESERVER

# Creating the Empty Tables in the Database f it doesn't exist yet
mk_dbenv()

# Querying servers from the Database and storing the results in a Ordered Dict
servers_query = Server().query_all()
srvs_dict = OrderedDict()
for entry in servers_query:
    srvs_dict[entry.name] = entry

# setting the Ansible Command
ans_cmd = [PLAYBOOKBIN, PBDIR + "lsserver.yml", "-l", targ_hosts]

# Calling Ansible process
print ('Trying to retrieve Servers info from Ansible Clients ...')
try:
    call(ans_cmd)
    print ('Success! Retrieved Servers info from Ansible Clients')
except OSError as err_msg:
    print('Could not execute "{}":\n{}'.format(ans_cmd, err_msg))

# Creating Server Classes from the Files generated from the Ansible Playbook
for filename in os.listdir(PBOUTPUTDIR):
    if filename.endswith(".pb"):
        host = os.path.basename(filename).replace(".pb", "")
        _file = open(os.path.join(PBOUTPUTDIR, filename))
        line = eval(_file.readline())

        print ('Parsing/Persisting Server: {} ...'.format(host))
        newserver = False
        changes_dict = []

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if host not in srvs_dict.keys():
            srvs_dict[host] = Server()
            srvs_dict[host].name = host
            newserver = True
            changes_dict.append(['LPAR', host, 'server', 'existent', 'non-existent', now])

        for prop in line:
            i, v = prop.split('=')
            if i == "IP Address":
                if srvs_dict[host].ipaddress != v and not newserver:
                    changes_dict.append(['Operating System', host, 'IP Address', v, srvs_dict[host].ipaddress, now])
                srvs_dict[host].ipaddress = v
            elif i == "Type":
                if srvs_dict[host].cpu_type != v and not newserver:
                    changes_dict.append(['LPAR', host, 'CPU Type', v, srvs_dict[host].cpu_type, now])
                srvs_dict[host].cpu_type = v
            elif i == "Mode":
                if srvs_dict[host].cpu_mode != v and not newserver:
                    changes_dict.append(['LPAR', host, 'CPU Mode', v, srvs_dict[host].cpu_mode, now])
                srvs_dict[host].cpu_mode = v
            elif i == "Entitled Capacity":
                if not newserver:
                    if round(float(srvs_dict[host].cores), 2) != round(float(v),2):
                        changes_dict.append(['LPAR', host, 'Entitled Cores', v, srvs_dict[host].cores, now])
                srvs_dict[host].cores = v
            elif i == "Online Virtual CPUs":
                if not newserver:
                    if int(srvs_dict[host].vprocs) != int(v):
                        changes_dict.append(['LPAR', host, 'Virtual Processors', v, srvs_dict[host].vprocs, now])
                srvs_dict[host].vprocs = int(v)
            elif i == "Online Memory":
                if srvs_dict[host].memory != v and not newserver:
                    changes_dict.append(['LPAR', host, 'Memory', v, srvs_dict[host].memory, now])
                srvs_dict[host].memory = v
            elif i == "Oslevel":
                if srvs_dict[host].oslevel != v and not newserver:
                    changes_dict.append(['Operating System', host, 'Oslevel', v, srvs_dict[host].oslevel, now])
                srvs_dict[host].oslevel = v
            elif i == "Cluster Name":
                if srvs_dict[host].cluster_name != v and not newserver:
                    changes_dict.append(['Operating System', host, 'Cluster Name', v, srvs_dict[host].cluster_name,now])
                srvs_dict[host].cluster_name = v

        # Persisting the Object and its attributes to the Database.
        srvs_dict[host].update()
        for change in changes_dict:
            server_changes = ServerChanges()
            server_changes.level = change[0]
            server_changes.server_name = change[1]
            server_changes.attribute_name = change[2]
            server_changes.new_value = change[3]
            server_changes.old_value = change[4]
            server_changes.detected_on = change[5]
            server_changes.update()
        print ('Success! Parsed/Persisted Server {}'.format(host))
### END OF MAIN PROGRAM
