from flask import Flask
from os.path import join, dirname, realpath
import os
import ConfigParser
from flask.ext.pymongo import PyMongo
from logging.handlers import RotatingFileHandler
from app.utils.mongo_utils import MongoUtils
from flask.ext.security import Security, MongoEngineUserDatastore, UserMixin, RoleMixin
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from bson.objectid import ObjectId
from flask_mongoengine import MongoEngine
from app.utils.mongo_utils import MongoUtils
from app.utils.user_mongo_utils import UserMongoUtils

UPLOAD_FOLDER =join(dirname(realpath(__file__)), 'static/uploads/')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
mongo = PyMongo()

login_manager = LoginManager()

# Initialize mongo access point
mongo_utils = MongoUtils(mongo)

user_utils = UserMongoUtils(mongo)

db = MongoEngine()

from app.mod_auth.model.user_model import User, Role

user_datastore = MongoEngineUserDatastore(db, User, Role)

security = Security()

bcrypt = Bcrypt()


def create_app():
    # Here we  create flask app
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # We load configurations
    load_config(app)

    # Configure logging
    configure_logging(app)

    login_manager.init_app(app)

    # Initialize mongoengine db instance
    db.init_app(app)

    # Initialize the app to work with MongoDB
    mongo.init_app(app, config_prefix='MONGO')

    security.init_app(app, user_datastore)
    # Init modules
    init_modules(app)
    return app


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.
    :param unicode user_id: user_id (email) user to retrieve
    """
    user = user_utils.get_user(user_id)
    return user


def load_config(app):
    ''' Reads the config file and loads configuration properties into the Flask app.
    :param app: The Flask app object.
    '''
    # Get the path to the application directory, that's where the config file resides.
    par_dir = os.path.join(__file__, os.pardir)
    par_dir_abs_path = os.path.abspath(par_dir)
    app_dir = os.path.dirname(par_dir_abs_path)

    # Read config file
    config = ConfigParser.RawConfigParser()
    config_filepath = app_dir + '/config.cfg'
    config.read(config_filepath)

    app.config['SERVER_PORT'] = config.get('Application', 'SERVER_PORT')

    # Authentication security
    app.config['SECURITY_LOGIN_USER_TEMPLATE'] = config.get('Authentication', 'LOGIN_USER_TEMPLATE_PATH')
    app.config['SECURITY_REGISTER_USER_TEMPLATE'] = config.get('Authentication', 'REGISTER_USER_TEMPLATE_PATH')
    app.config['SECURITY_REGISTERABLE'] = config.get('Authentication', 'CAN_REGISTER')
    app.config['SECURITY_CONFIRMABLE'] = config.get('Authentication', 'CONFIRM_EMAIL')
    app.config['SECURITY_SEND_REGISTER_EMAIL'] = config.get('Authentication', 'SEND_REGISTER_EMAIL')
    app.config['SECURITY_SEND_PASSWORD_CHANGE_EMAIL'] = config.get('Authentication', 'SEND_PASSWORD_CHANGE_EMAIL')
    app.config['SECURITY_CONFIRM_EMAIL_WITHIN'] = bool(config.get('Authentication', 'SEND_CONFIRM_EMAIL_WITHIN'))
    app.config['SECURITY_CHANGEABLE'] = config.get('Authentication', 'PASSWORD_CHANGEABLE')
    app.config['SECURITY_PASSWORD_HASH'] = config.get('Authentication', 'PASSWORD_HASH')
    app.config['SECURITY_PASSWORD_SALT'] = config.get('Authentication', 'PASSWORD_SALT')
    app.config['SECURITY_POST_LOGIN_VIEW'] = config.get('Authentication', 'POST_LOGIN_VIEW')

    # Set the secret key, keep this really secret, we use it to secure wtform filed data
    app.secret_key = config.get('Application', 'SECRET_KEY')

    # Mongo configuration
    app.config['MONGO_DBNAME'] = config.get('Mongo', 'DB_NAME')
    app.config['MONGODB_DB'] = config.get('Mongo', 'DB_NAME')
    app.config['MONGODB_PORT'] = int(config.get('Mongo', 'DB_PORT'))
    app.config['MONGODB_HOST'] = config.get('Mongo', 'DB_HOST')
    app.config['MONGO_PORT'] = config.get('Mongo', 'DB_PORT')
    app.config['MONGO_HOST'] = config.get('Mongo', 'DB_HOST')

    # Logging path might be relative or starts from the root.
    # If it's relative then be sure to prepend the path with the application's root directory path.
    log_path = config.get('Logging', 'PATH')
    if log_path.startswith('/'):
        app.config['LOG_PATH'] = log_path
    else:
        app.config['LOG_PATH'] = app_dir + '/' + log_path

    app.config['LOG_LEVEL'] = config.get('Logging', 'LEVEL').upper()


def configure_logging(app):
    ''' Configure the app's logging.
     param app: The Flask app object
    '''

    log_path = app.config['LOG_PATH']
    log_level = app.config['LOG_LEVEL']

    # If path directory doesn't exist, create it.
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create and register the log file handler.
    log_handler = RotatingFileHandler(log_path, maxBytes=250000, backupCount=5)
    log_handler.setLevel(log_level)
    app.logger.addHandler(log_handler)

    # First log informs where we are logging to. Bit silly but serves  as a confirmation that logging works.
    app.logger.info('Logging to: %s', log_path)

def init_modules(app):

    # Import blueprint modules
    from app.mod_main.views import mod_main
    from app.mod_whatis.views import mod_whatis
    from app.mod_auth.views import mod_auth
    from app.mod_admin.views import mod_admin
    from app.mod_project.views import mod_project
    from app.mod_statistics.views import mod_statistics
    app.register_blueprint(mod_auth)
    app.register_blueprint(mod_main)
    app.register_blueprint(mod_whatis)
    app.register_blueprint(mod_admin)
    app.register_blueprint(mod_project)
    app.register_blueprint(mod_statistics)