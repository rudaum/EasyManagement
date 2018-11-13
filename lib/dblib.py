#!/usr/bin/python
"""
- Purpose:
    A Library to Handle DB Transactions, mapped as Table -> Class ->  Object by SQLAlchemy

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
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
# --------------------------------------------------------------- #
### END OF MODULE IMPORTS
## DB Section
DBURI = "mysql://easymanager:q1w2e3r4@denotsl90.int.kn/easymanagement"
# DBURI = "mysql://easymanager:q1w2e3r4@localhost/easymanagement"
DBENGINE = create_engine(DBURI)
DBASE = declarative_base()
DBSession = sessionmaker(bind=DBENGINE)()
### END OF MODULE IMPORTS ###


### START OF FUNCTIONS DECLARATION
# --------------------------------------------------------------- #
def mk_dbenv():
    DBASE.metadata.create_all(DBENGINE)
# --------------------------------------------------------------- #


# --------------------------------------------------------------- #
def query_all_from(_class):
    """
    Purpose:
        Retrieves all entries from Database for a given Class/Table and stores it in a Dictionary

    Parameters:
    """
    result_dict = OrderedDict()
    # Feeding the dictionary with the already existing servers records.
    for entry in eval('DBSession.query({}).order_by({}.name)'.format(_class, _class)):
        result_dict[entry.name] = entry

    return result_dict
# --------------------------------------------------------------- #


# --------------------------------------------------------------- #
def destroy_table(_class):
    """
    Purpose:
        ** CAUTION ** This WILL destroy the Representative's Table and all its contents!
    Parameters:
    """
    global DBSession
    DBSession.execute(text('SET FOREIGN_KEY_CHECKS = 0;'))
    DBSession.close()
    _class.__table__.drop(DBENGINE)
    DBSession = sessionmaker(bind=DBENGINE)()
    DBSession.execute(text('SET FOREIGN_KEY_CHECKS = 1;'))
# ------------------------------------------------------- #


# --------------------------------------------------------------- #
def update_servers(hostsdict):
    """
    Purpose:
        Updates the 'servers' database with new or updates in the servers, based on the Objects in HOSTDICT dictionary

    Parameters:
        A Dictionary containing Server Instances
    """
    # Feeding the dictionary with the already existing servers records.
    for server in hostsdict.keys():
        # Updating the Database with the values.
        DBSession.add(hostsdict[server])
    DBSession.commit()
# --------------------------------------------------------------- #


# --------------------------------------------------------------- #
def update_users(usersdict):
    """
    Purpose:
        Updates the 'servers' database with new or updates in the servers, based on the Objects in HOSTDICT dictionary

    Parameters:
        A Dictionary containing Server Instances
    """
    # Feeding the dictionary with the already existing servers records.

    DBSession.rollback()
    for user in usersdict.keys():
        # Updating the Database with the values.
        DBSession.add(usersdict[user])
    DBSession.commit()
# --------------------------------------------------------------- #
### END OF FUNCTIONS DECLARATION ###


### START OF CLASSES DECLARATION ###
# --------------------------------------------------------------- #
class Cluster(DBASE):
    """
    Purpose:
        Represents a Cluster
    """
    __tablename__ = 'clusters'
    # Here we define columns for the table servers
    # Notice that each column is also a normal Python instance attribute.
    name = Column(String(20), primary_key=True)
    halevel = Column(String(12))
    cluster_type = Column(String(12))
    heartbeat_type = Column(String(12))
    cluster_nodes = Column(String(240), nullable=False)
    service_labels = Column(String(240))
    ipaddresses = Column(String(240))
    resource_groups = Column(String(240))
    startup_policy = Column(String(240))
    fallover_policy = Column(String(240))
    fallback_policy = Column(String(240))
    volume_groups = Column(String(240))
    applications = Column(String(240))
    start_scripts = Column(String(240))
    stop_scripts = Column(String(240))
    script_mode = Column(String(32))
    fs_before_ip = Column(String(240))
    user_defined_res = Column(String(240))

    def self_destruct(self):
        """
        Purpose:
            ** CAUTION ** This WILL destroy the Representative's Table and all its contents!
        Parameters:
        """
        self.__table__.drop(DBENGINE)

    def self_create(self):
        """
        Purpose:
            Creates the Representative's Table
        Parameters:
        """
        self.__table__.create(DBENGINE)

    def get_column_values(self, column):
        """
        Purpose:
            Retrieves the current value of this instance's column's value. But not from the DB
        Parameters:server
            column: The Columns's value to be retrieved.
        """
        return getattr(self, column)

    def get_columns(self):
        """
        Purpose:
            Retrieves the column names of a Class
        Parameters:
        """
        return self.__table__.columns.keys()

    def query_by(self, attr_name, attr_value):
        """
        Purpose:
            Queries the Database for all entries that match single Attribute and returns a list of results
        """
        query = eval('DBSession.query({}).filter({}.{} == "{}")'
                     .format(type(self).__name__, type(self).__name__, attr_name, attr_value))
        return query.all()

    def update(self):
        """
        Purpose:
            Updates and commits the database with the current Object Instance's Values
        """
        DBSession.add(self)
        DBSession.commit()

    def custom_query(self, custom_query):
        query = eval('DBSession.query({}).filter({})').format(type(self).__name__, custom_query)
        return query.all()

    def query_all(self):
        """
        Purpose:
            Retrieves all entries related to this Class from the Database and stores them in an Ordered Dictionary.

        Parameters:
        """
        hostsdict = OrderedDict()
        # Feeding the dictionary with the already existing Clusters records.
        for entry in DBSession.query(type(self)).order_by(type(self).name):
            hostsdict[entry.name] = entry
        return hostsdict
# --------------------------------------------------------------- #


# --------------------------------------------------------------- #
class Server(DBASE):
    """
    Purpose:
        Represents an AIX Server
    """
    __tablename__ = 'servers'
    # Here we define columns for the table servers
    # Notice that each column is also a normal Python instance attribute.
    name = Column(String(32), primary_key=True)
    ipaddress = Column(String(16))
    oslevel = Column(String(20))
    cores = Column(Integer)
    vprocs = Column(Integer)
    cpu_type = Column(String(20))
    cpu_mode = Column(String(20))
    memory = Column(String(20))
    cluster_name = Column(String(60))

    def self_destruct(self):
        """
        Purpose:
            ** CAUTION ** This WILL destroy the Representative's Table and all its contents!
        Parameters:
        """
        self.__table__.drop(DBENGINE)

    def self_create(self):
        """
        Purpose:
            Creates the Representative's Table
        Parameters:
        """
        self.__table__.create(DBENGINE)

    def get_column_values(self, column):
        """
        Purpose:
            Retrieves the current value of this instance's column's value. But not from the DB
        Parameters:
            column: The Columns's value to be retrieved.
        """
        return getattr(self, column)

    def get_columns(self):
        """
        Purpose:
            Retrieves the columns of a Class
        Parameters:
        """
        return self.__table__.columns.keys()

    def query_by(self, attr_name, attr_value):
        """
        Purpose:
            Queries the Database for all entries that match single Attribute and returns a list of results
        """
        query = eval('DBSession.query({}).filter({}.{} == "{}")'
                     .format(type(self).__name__, type(self).__name__, attr_name, attr_value))
        return query.all()

    def update(self):
        """
        Purpose:
            Updates and commits the database with the current Object Instance's Values
        """
        DBSession.add(self)
        DBSession.commit()

    def query(self, custom_query):
        query = eval('DBSession.query({}).filter({})').format(type(self).__name__, custom_query)
        return query.all()

    def query_all(self):
        """
        Purpose:
            Retrieves all entries related to this Class from Database and stores then in an Ordered Dictionary.

        Parameters:
        """
        hostsdict = OrderedDict()
        # Feeding the dictionary with the already existing servers records.
        for entry in DBSession.query(type(self)).order_by(type(self).name):
            hostsdict[entry.name] = entry
        return hostsdict
# --------------------------------------------------------------- #


# --------------------------------------------------------------- #
class User(DBASE):
    """
    Purpose:
        Represents an User from an AIX Server
    """
    __tablename__ = 'users'
    # Here we define columns for the table servers
    # Notice that each column is also a normal Python instance attribute.
    user_server = Column(String(256), primary_key=True)
    # user_server = Column(String(256), nullable=False, unique=True)
    server_name = Column(String(256), nullable=False)
    User_Name = Column(String(20), nullable=False)
    User_ID = Column(Integer, nullable=False)
    Primary_Group = Column(String(120))
    Groups = Column(String(120))
    Home = Column(String(256), nullable=False)
    Gecos = Column(String(256))
    time_last_login = Column(DateTime())
    maxage = Column(Integer)
    Shell = Column(String(256))
    umask = Column(Integer)
    fsize = Column(Integer)
    cpu = Column(Integer)
    data = Column(Integer)
    stack = Column(Integer)
    core = Column(Integer)
    rss = Column(Integer)
    nofiles = Column(Integer)
    login = Column(String(8))
    su = Column(String(8))
    rlogin = Column(String(8))
    daemon = Column(String(8))
    admin = Column(String(8))
    sugroups = Column(String(256))
    admgroups = Column(String(256))
    tpath = Column(String(12))
    ttys = Column(String(256))
    expires = Column(Integer)
    auth1 = Column(String(256))
    auth2 = Column(String(256))
    registry = Column(String(256))
    SYSTEM = Column(String(256))
    logintimes = Column(String(256))
    loginretries = Column(Integer)
    pwdwarntime = Column(Integer)
    account_locked = Column(String(8))
    minage = Column(Integer)
    maxexpired = Column(Integer)
    minalpha = Column(Integer)
    minother = Column(Integer)
    mindiff = Column(Integer)
    maxrepeats = Column(Integer)
    minlen = Column(Integer)
    histexpire = Column(Integer)
    histsize = Column(Integer)
    pwdchecks = Column(String(256))
    dictionlist = Column(String(256))
    default_roles = Column(String(256))
    roles = Column(String(256))

    def self_destruct(self):
        """
        Purpose:
            ** CAUTION ** This WILL destroy the Representative's Table and all its contents!
        Parameters:
        """
        self.__table__.drop(DBENGINE)

    def get_column_values(self, column):
        """
        Purpose:
            Retrieves the current value of this instance's column's value. But not from the DB
        Parameters:
            column: The Columns's value to be retrieved.
        """
        return getattr(self, column)

    def get_columns(self):
        """
        Purpose:
            Retrieves the columns of a Class Object
        Parameters:
        """
        return self.__table__.columns.keys()

    def query_by(self, attr_name, attr_value):
        """
        Purpose:
            Queries the Database for all entries that match single Attribute and returns a list of results
        """
        query = eval('DBSession.query({}).filter({}.{} == "{}")'
                     .format(type(self).__name__, type(self).__name__, attr_name, attr_value))
        return query.all()

    def update(self):
        """
        Purpose:
            Updates and commits the database with the current Object Instance's Values
        """
        DBSession.add(self)
        DBSession.commit()

    def query(self, custom_query):
        query = eval('DBSession.query({}).filter({})').format(type(self).__name__, custom_query)
        return query.all()

    def query_all(self):
        """
        Purpose:
            Retrieves all entries related to this Class from Database and stores them in an Ordered Dictionary

        Parameters:
        """
        ordered_dict = OrderedDict()
        # Feeding the dictionary with the already existing Users records.
        for entry in DBSession.query(type(self)).order_by(type(self).user_server):
            ordered_dict[entry.user_server] = entry
        return ordered_dict
# --------------------------------------------------------------- #


# --------------------------------------------------------------- #
class RPM(DBASE):
    """
    Purpose:
        Represents an User from an AIX Server
    """
    __tablename__ = 'rpms'
    # Here we define columns for the table servers
    # Notice that each column is also a normal Python instance attribute.
    rpm_server = Column(String(256), primary_key=True)
    server_name = Column(String(256), nullable=False)
    rpm = Column(String(256), nullable=False)
    version = Column(String(32), nullable=False)
    release = Column(String(32), nullable=False)
    build_date = Column(String(120))
    build_host = Column(String(120))
    relocations = Column(String(256))

    def self_destruct(self):
        """
        Purpose:
            ** CAUTION ** This WILL destroy the Representative's Table and all its contents!
        Parameters:
        """
        self.__table__.drop(DBENGINE)

    def get_column_values(self, column):
        """
        Purpose:
            Retrieves the current value of this instance's column's value. But not from the DB
        Parameters:
            column: The Columns's value to be retrieved.
        """
        return getattr(self, column)

    def get_columns(self):
        """
        Purpose:
            Retrieves the columns of a Class Object
        Parameters:
        """
        return self.__table__.columns.keys()

    def query_by(self, attr_name, attr_value):
        """
        Purpose:
            Queries the Database for all entries that match single Attribute and returns a list of results
        """
        query = eval('DBSession.query({}).filter({}.{} == "{}")'
                     .format(type(self).__name__, type(self).__name__, attr_name, attr_value))
        return query.all()

    def update(self):
        """
        Purpose:
            Updates and commits the database with the current Object Instance's Values
        """
        DBSession.add(self)
        DBSession.commit()

    def query(self, custom_query):
        query = eval('DBSession.query({}).filter({})').format(type(self).__name__, custom_query)
        return query.all()

    def query_all(self):
        """
        Purpose:
            Retrieves all entries related to this Class from Database and stores them in an Ordered Dictionary

        Parameters:
        """
        ordered_dict = OrderedDict()
        # Feeding the dictionary with the already existing RPM records.
        for entry in DBSession.query(type(self)).order_by(type(self).rpm_server):
            ordered_dict[entry.rpm_server] = entry
        return ordered_dict
# --------------------------------------------------------------- #
