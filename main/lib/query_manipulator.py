#!/usr/bin/python
"""
- Purpose:
    To Manipulate the Queries from the Database. There is a Collection Manipulator for each Table in the DB

- Author:
    Rudolf Wolter (KN OSY Team)

- Contact for questions and/or comments:
    rudolf.wolter@kuehne-nagel.com

- Version Releases and modifications.
    > 1.0 (17.09.2018) - Initial release with core functions.

- TODO:

"""
### START OF MODULE IMPORTS ###
# --------------------------------------------------------------- #
from dblib import Server, User, UserChanges, RPM, RPMChanges
from collections import OrderedDict
# --------------------------------------------------------------- #
### END OF MODULE IMPORTS

### START OF FUNCTIONS DECLARATION
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
### END OF FUNCTIONS DECLARATION ###


### START OF CLASSES DECLARATION ###
# --------------------------------------------------------------- #
class ServersManipulator:
    """
    Purpose:
        To manipulate the Servers data gathered in a DB query
    """

    def __init__(self, servers_query):
        self.servers_query = servers_query

    def get_servers_names(self):
        result = []
        for server in self.servers_query:
            result.append(server.name)
        return result

    def get_by_pkey(self, _key):
        result = None
        for obj in self.servers_query:
            if obj.name == _key:
                result = obj
                break
        return result

    def get_columns(self):
        result = Server().get_columns()
        return result
# --------------------------------------------------------------- #


# --------------------------------------------------------------- #
class ServerChangeLogManipulator:
    """
    Purpose:
        To manipulate the data gathered in a DB query
    """
    query_list = []

    def __init__(self, change_log_query):
        self.change_log_query = change_log_query
        self.query_list = []
        for entry in self.change_log_query:
            self.query_list.append([entry.server_name,
                                    entry.id,
                                    entry.level,
                                    entry.attribute_name,
                                    entry.new_value,
                                    entry.old_value,
                                    entry.detected_on,
                                    "Server Change"
                                    ])

    def get_columns(self):
        result = UserChanges().get_columns()
        return result

    def get_uniq_servers(self):
        result = []
        for changes in self.query_list:
            if changes[0] not in result:
                result.append(changes[0])
        return result

    def filter_by_server(self, server='-ALL-'):
        result = []
        for change in self.query_list:
            if change[0] == server or server == '-ALL-':
                result.append(change)
        return result
# --------------------------------------------------------------- #


# --------------------------------------------------------------- #
class UsersManipulator:
    """
    Purpose:
        To manipulate the data gathered in a DB query
    """

    def __init__(self, users_query):
        self.users_query = users_query

    def get_servers_by_user(self, user):
        result = []
        for user_server in self.users_query:
            if user_server.user_name == user:
                result.append(user_server.server_name)
        return result

    def get_by_pkey(self, _key):
        result = self.users_query[_key]
        return result

    def get_uniq_users(self):
        result = []
        for user_server in self.users_query:
            if user_server.user_name not in result:
                result.append(user_server.user_name)
        return result

    def get_columns(self):
        result = User().get_columns()
        return result

    def get_servers(self, user='root'):
        result = []
        for user_server in self.users_query:
            if user_server.user_name == user:
                result.append(user_server)
        return result

    def get_users_by_server(self, server):
        result = []
        for user_server in self.users_query:
            if user_server.server_name == server:
                result.append(user_server)
        return result

    def get_usernames_by_server(self, server):
        result = []
        for user_server in self.users_query:
            if user_server.server_name == server:
                result.append(user_server.user_name)
        return result

    def dictionarize(self):
        user_dict = OrderedDict()
        for user_server in self.users_query:
            if user_server.server_name not in user_dict:
                user_dict[user_server.server_name] = OrderedDict()
            else:
                user_dict[user_server.server_name][user_server.user_name] = user_server

        return user_dict

    def dictionarize_by_server(self, server):
        user_dict = OrderedDict()
        for user_server in self.users_query:
            if user_server.server_name == server:
                if user_server.server_name not in user_dict:
                    user_dict[user_server.server_name] = OrderedDict()
                user_dict[user_server.server_name][user_server.user_name] = user_server
        return user_dict
# --------------------------------------------------------------- #


# --------------------------------------------------------------- #
class UserChangeLogManipulator:
    """
    Purpose:
        To manipulate the data gathered in a DB query
    """
    query_list = []

    def __init__(self, change_log_query):
        self.change_log_query = change_log_query
        self.query_list = []
        for entry in self.change_log_query:
            self.query_list.append([entry.server_name,
                                    entry.id,
                                    entry.user_name,
                                    entry.attribute_name,
                                    entry.new_value,
                                    entry.old_value,
                                    entry.detected_on,
                                    "User Change"
                                    ])

    def get_columns(self):
        result = UserChanges().get_columns()
        return result

    def get_all_columns_but(self, col):
        result = self.get_columns()
        result.remove(col)
        return result

    def get_uniq_users(self):
        result = []
        for changes in self.query_list:
            if changes[2] not in result:
                result.append(changes[2])
        return result

    def get_uniq_servers(self):
        result = []
        for changes in self.query_list:
            if changes[0] not in result:
                result.append(changes[0])
        return result

    def filter_by_user(self, user):
        result = []
        for changes in self.query_list:
            if changes[2] == user or user == '-ALL-':
                result.append(changes)
        return result

    def filter_by_server(self, server='-ALL-'):
        result = []
        for change in self.query_list:
            if change[0] == server or server == '-ALL-':
                result.append(change)
        return result

    def get_servers_by_user(self, user='-ALL-'):
        result = []
        for changes in self.query_list:
            if (changes[0] == user or user == '-ALL-') and changes[0] not in result:
                result.append(changes[0])
        result.sort()
        return result
# --------------------------------------------------------------- #


# --------------------------------------------------------------- #
class RPMsManipulator:
    """
    Purpose:
        To manipulate the RPM data gathered in a DB query
    """
    def __init__(self, rpm_query):
        self.rpm_query = rpm_query

    def get_uniq_rpms(self):
        result = []
        for rpm in self.rpm_query:
            if rpm.rpm not in result:
                result.append(rpm.rpm)
        return result

    def get_uniq_servers(self):
        result = []
        for rpm in self.rpm_query:
            if rpm.server_name not in result:
                result.append(rpm.server_name)
        return result

    def get_by_pkey(self, _key):
        result = None
        for obj in self.rpm_query:
            if obj.name == _key:
                result = obj
                break
        return result

    def get_columns(self):
        result = RPM().get_columns()
        return result

    def filter_by_server(self, server='-ALL-'):
        result = []
        for rpm_entry in self.rpm_query:
            if rpm_entry.server_name == server or server == '-ALL-':
                result.append(rpm_entry)
        return result

    def get_rpm(self, rpm):
        result = []
        for rpm_server in self.rpm_query:
            if rpm_server.rpm == rpm:
                result.append(rpm_server)
        return result

    def dictionarize_by_server(self, server):
        dict = OrderedDict()
        for rpm_server in self.rpm_query:
            if rpm_server.server_name == server:
                if rpm_server.server_name not in dict:
                    dict[rpm_server.server_name] = OrderedDict()
                dict[rpm_server.server_name][rpm_server.rpm] = rpm_server
        return dict
# --------------------------------------------------------------- #


# --------------------------------------------------------------- #
class RPMChangeLogManipulator:
    """
    Purpose:
        To manipulate the data gathered in a DB query
    """
    query_list = []

    def __init__(self, change_log_query):
        self.change_log_query = change_log_query
        self.query_list = []
        for entry in self.change_log_query:
            self.query_list.append([entry.server_name,
                                    entry.id,
                                    entry.rpm_name,
                                    entry.attribute_name,
                                    entry.new_value,
                                    entry.old_value,
                                    entry.detected_on,
                                    "RPM Change"
                                    ])

    def get_columns(self):
        result = RPMChanges().get_columns()
        return result

    def get_all_columns_but(self, col):
        result = self.get_columns()
        result.remove(col)
        return result

    def get_uniq_rpms(self):
        result = []
        for changes in self.query_list:
            if changes[2] not in result:
                result.append(changes[2])
        return result

    def get_uniq_servers(self):
        result = []
        for changes in self.query_list:
            if changes[0] not in result:
                result.append(changes[0])
        return result

    def filter_by_rpm(self, rpm):
        result = []
        for changes in self.query_list:
            if changes[2] == rpm or rpm == '-ALL-':
                result.append(changes)
        return result

    def filter_by_server(self, server='-ALL-'):
        result = []
        for change in self.query_list:
            if change[0] == server or server == '-ALL-':
                result.append(change)
        return result

    def get_servers_by_rpm(self, rpm='-ALL-'):
        result = []
        for changes in self.query_list:
            if (changes[0] == rpm or rpm == '-ALL-') and changes[0] not in result:
                result.append(changes[0])
        result.sort()
        return result
# --------------------------------------------------------------- #
