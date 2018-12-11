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
from dblib import User, UserChanges
# --------------------------------------------------------------- #
### END OF MODULE IMPORTS

### START OF FUNCTIONS DECLARATION
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
### END OF FUNCTIONS DECLARATION ###


### START OF CLASSES DECLARATION ###
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
        for user_server in self.users_query.items():
            if user_server[1].user_name == user:
                result.append(user_server[1].server_name)
        return result

    def get_by_pkey(self, _key):
        result = self.users_query[_key]
        print type(result)
        return result

    def get_uniq_users(self):
        result = []
        for user_server in self.users_query.items():
            if user_server[1].user_name not in result:
                result.append(user_server[1].user_name)
        return result

    def get_columns(self):
        result = User().get_columns()
        return result

    def get_servers(self, user='root'):
        result = []
        for user_server in self.users_query.items():
            if user_server[1].user_name == user:
                result.append(user_server[1])
        return result

class ChangeLogManipulator:
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
                                    entry.detected_on
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

    def get_servers_by_user(self, user='-ALL-'):
        result = []
        for changes in self.query_list:
            if (changes[2] == user or user == '-ALL-') and changes[0] not in result:
                result.append(changes[0])
        result.sort()
        return result