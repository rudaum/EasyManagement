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

path = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(path + '/../../')
from subprocess import call
from main.lib.dblib import mkDbenv, Cluster
from main.lib.settings import PLAYBOOKBIN, PBDIR, SAFESERVER
# --------------------------------------------------------------- #
### END OF MODULE IMPORTS

### START OF GLOBAL VARIABLES DECLARATION
# --------------------------------------------------------------- #
## General Vars
ARGS = sys.argv
NARGS = len(ARGS[1:])
PBOUTPUTDIR = PBDIR + "output/lscluster/"
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
    Executes the Ansible Playbook responsible for retrieving General Cluster information from Ansible clients.
    Stores the information in the Server Objects hosted by the HOSTDICT Global variable for later DB transactions

Parameters:
    targ_hosts: The Ansibles Clients that will have their information collected
"""

# If no Target Hosts are given, then use a SAFE host as security measure
targ_hosts = ARGS[1] if NARGS > 0 else SAFESERVER

# Creating the Empty Tables in the Database f it doesn't exist yet
mkDbenv()

# Querying servers from the Database and storing the results in a Ordered Dict
cluster_dict = Cluster().queryAll()

# setting the Ansible Command
ans_cmd = [PLAYBOOKBIN, PBDIR + "lscluster.yml", "-l", targ_hosts]

# Calling Ansible process
call(ans_cmd)

# Creating Cluster Classes from the Files generated from the Ansible Playbook
for filename in os.listdir(PBOUTPUTDIR):
    if filename.endswith(".pb"):
        host = os.path.basename(filename).replace(".pb", "")
        file = open(os.path.join(PBOUTPUTDIR, filename))
        line = eval(file.readline())
        for prop in line:
            i, v = prop.split('=')
            if i == "cluster_name":
                cluster = v
                if cluster not in cluster_dict.keys():
                    cluster_dict[cluster] = Cluster()
                    cluster_dict[cluster].name = cluster
            elif i == "halevel":
                cluster_dict[cluster].halevel = v
            elif i == "cluster_type":
                cluster_dict[cluster].cluster_type = v
            elif i == "heartbeat_type":
                cluster_dict[cluster].heartbeat_type = v
            elif i == "cluster_nodes":
                cluster_dict[cluster].cluster_nodes = v
            elif i == "service_labels":
                cluster_dict[cluster].service_labels = v
            elif i == "ipaddresses":
                cluster_dict[cluster].ipaddresses = v
            elif i == "resource_groups":
                cluster_dict[cluster].resource_groups = v
            elif i == "startup_policy":
                cluster_dict[cluster].startup_policy = v
            elif i == "fallover_policy":
                cluster_dict[cluster].fallover_policy = v
            elif i == "fallback_policy":
                cluster_dict[cluster].fallback_policy = v
            elif i == "volume_groups":
                cluster_dict[cluster].volume_groups = v
            elif i == "applications":
                cluster_dict[cluster].applications = v
            elif i == "start_scripts":
                cluster_dict[cluster].start_scripts = v
            elif i == "stop_scripts":
                cluster_dict[cluster].stop_scripts = v
            elif i == "script_mode":
                cluster_dict[cluster].script_mode = v
            elif i == "fs_before_ip":
                cluster_dict[cluster].fs_before_ip = v
            elif i == "user_defined_res":
                cluster_dict[cluster].user_defined_res = v

        # Persisting the Object and its attributes to the Database.
        cluster_dict[cluster].update()
### END OF MAIN PROGRAM
