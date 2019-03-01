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
import os
import sys
path = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '../..')
sys.path.append(path)
from flask import Flask
from tools.blueprints.page import page
from lib.threadlib import start_dbquery_thread
# --------------------------------------------------------------- #
### END OF MODULE IMPORTS ###

### START OF GLOBAL VARIABLES DECLARATION ###
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
### END OF GLOBAL VARIABLES DECLARATION ###


### START OF UTILITY FUNCTIONS DECLARATION
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
### END OF UTILITY FUNCTIONS DECLARATION

# Starting the DB thread that refreshes the QUERY global variables
start_dbquery_thread()

# instantiating the Flask Application, with relative configuration enabled
app = Flask(__name__, instance_relative_config=True)

# Setting some configurations
app.config.from_object('main.lib.settings')

# Calling the Main Page Blueprints
app.register_blueprint(page)

# Starting the Web Application
app.run(threaded=True)
