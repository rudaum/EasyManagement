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
from main.lib.settings import PLAYBOOKBIN, PBDIR, SAFESERVER
from main.lib.dblib import mk_dbenv, RPM

# --------------------------------------------------------------- #
### END OF MODULE IMPORTS

### START OF GLOBAL VARIABLES DECLARATION
# -----------------------------------------dblib.Server().queryBy('name', 'sindbad1')---------------------- #
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
ordered_dict = RPM().query_all()

# setting the Ansible Command
ans_cmd = [PLAYBOOKBIN, PBDIR + "lsrpm.yml", "-l", targ_hosts]

# Calling Ansible process
call(ans_cmd)

# Creating Server Classes from the Files generated from the Ansible Playbook
for filename in os.listdir(PBOUTPUTDIR):
    if filename.endswith(".pb"):
        host = os.path.basename(filename).replace(".pb", "")
        file = open(os.path.join(PBOUTPUTDIR, filename))
        list = eval('[' + file.readline().replace(', "-NEXT-", ', '],[').replace(', "-NEXT-"]', ']') + ']')
        for item in list:
            name = item[0].split('=')[1]
            dictidx = name + '_' + host
            if dictidx not in ordered_dict.keys():
                ordered_dict[dictidx] = RPM()
            ordered_dict[dictidx].rpm_server = dictidx
            ordered_dict[dictidx].rpm = name
            ordered_dict[dictidx].server_name = host
            for attribute in item[1:]:
                attr = attribute.split('=')[0]
                value = attribute.split('=')[1] if len(attribute.split('=')[1]) > 0 else ' '  # Skipping empty attr.
                if attr == "Version":
                    ordered_dict[dictidx].version = value
                elif attr == "Release":
                    ordered_dict[dictidx].release = value
                elif attr == "Build Date":
                    ordered_dict[dictidx].build_date = value
                elif attr == "Build Host":
                    ordered_dict[dictidx].build_host = value
                elif attr == "Relocations":
                    ordered_dict[dictidx].relocations = value
        # Persisting the RPM Object into the database
        ordered_dict[dictidx].update()
### END OF MAIN PROGRAM
