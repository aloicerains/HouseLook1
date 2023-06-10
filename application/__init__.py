
from flask import Flask

import os
import flask_login
from flask_login import LoginManager



application = Flask(__name__)
application.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'admin_login'


from application import routes