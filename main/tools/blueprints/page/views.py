### START OF MODULE IMPORTS ###
# --------------------------------------------------------------- #
from collections import OrderedDict
from flask import Blueprint, render_template
from main.lib.dblib import User, RPM
from main.lib.threadlib import ALL_SERVERS_FROM_DB, \
    ALL_USERS_FROM_DB, ALL_RPMS_FROM_DB, ALL_USER_CHANGES,\
    ALL_SERVERS_CHANGES, ALL_RPM_CHANGES

### START OF GLOBAL VARIABLES DECLARATION
# --------------------------------------------------------------- #
# Creating the Template Env
page = Blueprint('page', __name__, template_folder='templates')
# --------------------------------------------------------------- #
### END OF GLOBAL VARIABLES DECLARATION ###


### START OF UTILITY FUNCTIONS DECLARATION
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
### END OF UTILITY FUNCTIONS DECLARATION

# --- INDEX PAGE --- #
@page.route('/', methods=['GET'])
def home():
    num_servers = len(ALL_SERVERS_FROM_DB.get_servers_names())
    num_users = len(ALL_USERS_FROM_DB.get_uniq_users())
    num_rpms = len(ALL_RPMS_FROM_DB.get_uniq_rpms())
    servers_names = ALL_SERVERS_FROM_DB.get_servers_names()
    return render_template('index.html', servers_names=servers_names,
                           num_servers=num_servers, num_users=num_users, num_rpms=num_rpms)
# ------------------- #


# --- SERVERS PAGE --- #
@page.route('/servers', methods=['GET', 'POST'])
def servers(server='ALL'):
    return render_template('servers.html', server_man=ALL_SERVERS_FROM_DB, server=server)
# ------------------- #


# --- SERVER DETAILS PAGE --- #
@page.route('/servers/<server>', methods=['GET', 'POST'])
def server_details(server):
    queried_server = ALL_SERVERS_FROM_DB.get_by_pkey(server)
    if not server or not queried_server:
        return render_template('servers.html', server_man=ALL_SERVERS_FROM_DB, server="ALL")
    else:
        server_changes = ALL_USER_CHANGES.filter_by_server(queried_server.name)
        server_changes.extend(ALL_SERVERS_CHANGES.filter_by_server(queried_server.name))
        server_changes.extend(ALL_RPM_CHANGES.filter_by_server(queried_server.name))

        # Sorting changes as Date Descending
        switch = True
        while switch:
            switch = False
            for i in range(0, len(server_changes) - 1):
                if len(server_changes) > 1:
                    if server_changes[i][6] < server_changes[i + 1][6]:
                        server_changes.insert(i, server_changes.pop(i + 1))
                        switch = True

        if len(server_changes) < 5:
            for i in range(len(server_changes), 5):
                server_changes.append(['-', '-', '-', '-', '-', '-', '-', '-'])
        return render_template('server_details.html', server_man=ALL_SERVERS_FROM_DB,
                               server=queried_server,
                               users=ALL_USERS_FROM_DB.get_users_by_server(queried_server.name),
                               server_changes=server_changes,
                               rpms=ALL_RPMS_FROM_DB.filter_by_server(queried_server.name)
                               )
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


# --- RPMS PAGE --- #
@page.route('/rpms', methods=['GET', 'POST'])
@page.route('/rpms/<rpm>', methods=['GET', 'POST'])
def rpms(rpm='AIX-rpm'):
    rpm_query = ALL_RPMS_FROM_DB.get_rpm(rpm)
    uniq_rpms = ALL_RPMS_FROM_DB.get_uniq_rpms()
    return render_template('rpms.html',
                           rpm_query=rpm_query,
                           uniq_rpms=uniq_rpms,
                           rpm=rpm
                           )
# ------------------- #


# --- RPM CHANGE-LOG PAGE --- #
@page.route('/rpms-changelog', methods=['GET', 'POST'])
@page.route('/rpms-changelog/<rpm>', methods=['GET', 'POST'])
def rpm_changelog(rpm='-ALL-'):
    return render_template('rpms-changelog.html', rpm=rpm, rpm_changes=ALL_RPM_CHANGES)
# ------------------- #


# --- COMPARISON PAGE --- #
@page.route('/compare/<parameters>', methods=['GET', 'POST'])
def compare(parameters):
    servers_to_compare = parameters.split('&')[0].split('=')[1].split(',')
    modules_to_compare = parameters.split('&')[1].split('=')[1].split(',')
    servers_users_query = OrderedDict()
    users_from_server = OrderedDict()
    uniq_users = set()
    servers_rpms_query = OrderedDict()
    rpms_from_server = OrderedDict()
    uniq_rpms = set()

    # Getting Users from the DB query based on the selected servers
    if 'users' in modules_to_compare:
        for server in servers_to_compare:
            # creating a dictionary out of the queried Users objects
            servers_users_query.update(ALL_USERS_FROM_DB.dictionarize_by_server(server))

            # Getting the Uniq Users from the latest compared server
            uniq_users.update(set(servers_users_query.values()[len(servers_users_query) - 1].keys()))

            # Dictionary of user names only for each compared server
            users_from_server[server] = servers_users_query.values()[len(servers_users_query) - 1].keys()

        # Looping over Servers to get User names that doesn't exit in the Unique users list.
        for server, usernames in users_from_server.items():
            for diff in uniq_users.difference(usernames):
                servers_users_query[server][diff] = User()
                for attr in servers_users_query[server][diff].get_columns():
                    setattr(servers_users_query[server][diff], attr, '-')

    # Getting RPMs from the DB query based on the selected servers
    if 'rpms' in modules_to_compare:
        for server in servers_to_compare:
            # creating a dictionary out of the queried RPM objects
            servers_rpms_query.update(ALL_RPMS_FROM_DB.dictionarize_by_server(server))

            # Getting the Uniq RPMS from the latest compared server
            uniq_rpms.update(set(servers_rpms_query.values()[len(servers_rpms_query) - 1].keys()))

            # Dictionary of RPM names only, for each compared server
            rpms_from_server[server] = servers_rpms_query.values()[len(servers_rpms_query) - 1].keys()

        # Looping over Servers to get User names that doesn't exit in the Unique users list.
        for server, rpmnames in rpms_from_server.items():
            for diff in uniq_rpms.difference(rpmnames):
                servers_rpms_query[server][diff] = RPM()
                for attr in servers_rpms_query[server][diff].get_columns():
                    setattr(servers_rpms_query[server][diff], attr, '-')

    return render_template('compare.html',
                           servers_to_compare=servers_to_compare,
                           modules_to_compare=modules_to_compare,
                           servers_users_query=servers_users_query,
                           servers_rpms_query=servers_rpms_query,
                           uniq_users=sorted(uniq_users),
                           uniq_rpms=sorted(uniq_rpms)
                           )
# ------------------- #
