#!/usr/bin/python
# - Purpose:
#       <purpose>
# - Author:
#       <author>
# - Contact for questions and/or comments:
#       <contact>
# - Parameters:
#       < accepted arguments>
# - Version Releases and modifications.
#       <versions history log>

### START OF MODULE IMPORTS ###
# --------------------------------------------------------------- #
import threading
import time
from main.lib.dblib import Server, ServerChanges, User, UserChanges, RPM, RPMChanges
from main.lib.query_manipulator import UsersManipulator, UserChangeLogManipulator, \
    ServersManipulator, ServerChangeLogManipulator, \
    RPMsManipulator, RPMChangeLogManipulator
# --------------------------------------------------------------- #
### END OF MODULE IMPORTS ###

### START OF GLOBAL VARIABLES DECLARATION ###
# --------------------------------------------------------------- #
ALL_SERVERS_FROM_DB = ServersManipulator(Server().query_all())
ALL_SERVERS_CHANGES = ServerChangeLogManipulator(ServerChanges().query_all())
ALL_USERS_FROM_DB = UsersManipulator(User().query_all())
ALL_USER_CHANGES = UserChangeLogManipulator(UserChanges().query_all())
ALL_RPMS_FROM_DB = RPMsManipulator(RPM().query_all())
ALL_RPM_CHANGES = RPMChangeLogManipulator(RPMChanges().query_all())
# --------------------------------------------------------------- #
### END OF GLOBAL VARIABLES DECLARATION ###


### START OF UTILITY FUNCTIONS DECLARATION
# --------------------------------------------------------------- #
def set_global_vars():
    while True:
        global ALL_SERVERS_FROM_DB, ALL_SERVERS_CHANGES, \
            ALL_USERS_FROM_DB, ALL_USER_CHANGES, \
            ALL_RPMS_FROM_DB, ALL_RPM_CHANGES
        ALL_SERVERS_FROM_DB = ServersManipulator(Server().query_all())
        ALL_SERVERS_CHANGES = ServerChangeLogManipulator(ServerChanges().query_all())
        ALL_USERS_FROM_DB = UsersManipulator(User().query_all())
        ALL_USER_CHANGES = UserChangeLogManipulator(UserChanges().query_all())
        ALL_RPMS_FROM_DB = RPMsManipulator(RPM().query_all())
        ALL_RPM_CHANGES = RPMChangeLogManipulator(RPMChanges().query_all())
        time.sleep(60)
# --------------------------------------------------------------- #
### END OF UTILITY FUNCTIONS DECLARATION


def start_dbquery_thread():
    set_vars_thread = threading.Thread(target=set_global_vars)
    # set_vars_thread.name = time.time()
    set_vars_thread.start()
