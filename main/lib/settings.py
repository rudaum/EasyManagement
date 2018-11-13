import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql://easymanager:q1w2e3r4@denotsl90.int.kn/easymanagement'
SQLALCHEMY_TRACK_MODIFICATIONS = True
PLAYBOOKBIN = "/usr/bin/ansible-playbook"
PBDIR = os.path.dirname(os.path.realpath(__file__)) + "/../playbooks/"
SAFESERVER = 'denotsp40'
NULLSTR = '-null-'