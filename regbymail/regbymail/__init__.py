# coding = utf-8

##################
#### imports #####
##################

import os

from flask import Flask, render_template
# pip3 install flask-login
from flask_login import LoginManager
# pip3 install flask-bcrypt
from flask_bcrypt import Bcrypt
# pip3 install flask-mail
from flask_mail import Mail

# pip3 install flask-debugtoolbar
from flask_debugtoolbar import DebugToolbarExtension

# import dbutils
from .dbutils import get_db_session

#create werzeug instance
app = Flask(__name__)
app.config.from_object('config')

bcrypt = Bcrypt(app)
from .models import User

#create db connection
connectionstr = app.config['SQLALCHEMY_DATABASE_URI']
session = get_db_session(connectionstr)

login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail(app)
toolbar = DebugToolbarExtension(app)

from .testv.views import testv_blueprint
app.register_blueprint(testv_blueprint)

from .main.views import main_blueprint
app.register_blueprint(main_blueprint)

from .user.views import user_blueprint
app.register_blueprint(user_blueprint)

from . import user
login_manager.login_view = "user.login"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).filter(User.id == int(user_id)).first()

@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500

