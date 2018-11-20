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
from collections import OrderedDict
from dblib import User
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






