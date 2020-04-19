from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
import stripe

app = Flask(__name__)
app.config['SECRET_KEY'] = '2912d4c2b6692117365c6cea'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "jainaryaman123@gmail.com"
app.config['MAIL_PASSWORD'] = "Vicky26jan"
mail = Mail(app)

from lecyc import routes
from lecyc.errors.handlers import errors
app.register_blueprint(errors)

# return app
