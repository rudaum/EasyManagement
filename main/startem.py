"""
Sets and starts the Flask Application using Blueprints

:return: Running Flask Application
"""
import sys, os
path = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '../..')
sys.path.append(path)
from flask import Flask
from tools.blueprints.page import page

# instantiating the Flask Application, with relative configuration enabled
app = Flask(__name__, instance_relative_config=True)

# Setting some configurations
app.config.from_object('main.lib.settings')

# Calling the Main Page Blueprints
app.register_blueprint(page)

# Starting the Web Application
app.run()
