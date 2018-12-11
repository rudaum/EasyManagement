### START OF MODULE IMPORTS ###
# --------------------------------------------------------------- #
from flask import Blueprint, render_template
from main.lib.dblib import Server, User, UserChanges
from main.lib.query_manipulator import UsersManipulator, ChangeLogManipulator
### END OF MODULE IMPORTS ###

### START OF GLOBAL VARIABLES DECLARATION
# --------------------------------------------------------------- #
# Creating the Template Env
page = Blueprint('page', __name__, template_folder='templates')
ALL_USERS_FROM_DB = UsersManipulator(User().query_all())
ALL_USER_CHANGES = ChangeLogManipulator(UserChanges().query_all())
# --------------------------------------------------------------- #
### END OF GLOBAL VARIABLES DECLARATION ###


# --- INDEX PAGE --- #
@page.route('/', methods=['GET'])
def home():
    servers_dict = Server().query_all()
    return render_template('index.html', servers_dict=servers_dict)
# ------------------- #


# --- SERVERS PAGE --- #
@page.route('/servers', methods=['GET', 'POST'])
@page.route('/servers/<server>', methods=['GET', 'POST'])
def servers(server=None):
    servers_dict = Server().query_all()
    return render_template('servers.html', servers_dict=servers_dict, server=server)
# ------------------- #


# --- USERS PAGE --- #
@page.route('/users', methods=['GET', 'POST'])
@page.route('/users/<user>', methods=['GET', 'POST'])
def users(user='root'):
    user_query = ALL_USERS_FROM_DB.get_servers(user)
    uniq_users = ALL_USERS_FROM_DB.get_uniq_users()
    return render_template('users.html',
                           user_query=user_query,
                           uniq_users=uniq_users,
                           user=user
                           )
# ------------------- #


# --- USER CHANGE-LOG PAGE --- #
@page.route('/users-changelog', methods=['GET', 'POST'])
@page.route('/users-changelog/<user>', methods=['GET', 'POST'])
def user_changelog(user='-ALL-'):
    return render_template('users-changelog.html', user=user, user_changes=ALL_USER_CHANGES)
# ------------------- #
