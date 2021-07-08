from datetime import datetime
import os

# import json
from flask import Flask, session
# from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from flask_user import UserManager
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

# Instantiate Flask extensions
db = SQLAlchemy()
csrf_protect = CSRFProtect()
# mail = Mail()
migrate = Migrate()

from config import DevelopmentConfig

# from app.simple_page import simple_page

bootstrap = Bootstrap()
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# login_manager.login_manager_message = 'Please log in to access this page.'


def create_app(config_class=DevelopmentConfig):
    # Instantiate Flask
    app = Flask(__name__,
                # static_folder='./sb_admin',
                # template_folder='./app/templates'
                )

    # Load App Config settings
    # Load common settings from 'app/settings.py' file
    # app.config.from_object('app.settings')
    # Load local settings from 'app/local_settings.py'
    # app.config.from_object('app.local_settings')
    # Load extra config settings from 'extra_config_settings' param
    # app.config.update(extra_config_settings)
    app.config.from_object(config_class)

    bootstrap.init_app(app)

    # Database to use flask db
    # Setup Flask-SQLAlchemy
    db.init_app(app)
    # Setup Flask-Migrate
    migrate.init_app(app, db)
    # Setup Flask-Mail
    # mail.init_app(app)
    # Setup session
    Session(app)
    # Setup WTForms CSRFProtect
    csrf_protect.init_app(app)

    # login_manager = LoginManager()
    # login_manager.init_app( app )

    # Add modules/packages
    # Register blueprints
    # from app.auth import bp as auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    #
    # from app.main import bp as main_bp
    # app.register_blueprint(main_bp)
    #
    # from app.admin import mod as admin
    # app.register_blueprint(admin, url_prefix='/admin')

    from app.controllers.controller1 import main_blueprint
    from app.controllers.apis import api_blueprint
    # from app.controllers.controller2 import controller2_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint)
    # app.register_blueprint(controller2_blueprint)
    csrf_protect.exempt(api_blueprint)

    # Setup Flask-User to handle user account related forms
    # from .models.user_models import User, MyRegisterForm
    # from .controllers.controller1 import user_profile_page

    # user_manager = UserManager(app, db, User)
    login_manager = LoginManager( app )
    # login_manager = LoginManager( app )
    # login_manager.init_app( app )

    @login_manager.user_loader
    def load_user(user_id):
        return user_id

    return app

def init_email_error_handler(app):
    """
    Initialize a logger to send emails on error-level messages.
    Unhandled exceptions will now send an email message to app.config.ADMINS.
    """
    if app.debug: return  # Do not send error emails while developing

    # Retrieve email settings from app.config
    host = app.config['MAIL_SERVER']
    port = app.config['MAIL_PORT']
    from_addr = app.config['MAIL_DEFAULT_SENDER']
    username = app.config['MAIL_USERNAME']
    password = app.config['MAIL_PASSWORD']
    secure = () if app.config.get('MAIL_USE_TLS') else None

    # Retrieve app settings from app.config
    to_addr_list = app.config['ADMINS']
    subject = app.config.get('APP_SYSTEM_ERROR_SUBJECT_LINE', 'System Error')

    # Setup an SMTP mail handler for error-level messages
    import logging
    from logging.handlers import SMTPHandler

    mail_handler = SMTPHandler(
        mailhost=(host, port),  # Mail host and port
        fromaddr=from_addr,  # From address
        toaddrs=to_addr_list,  # To address
        subject=subject,  # Subject line
        credentials=(username, password),  # Credentials
        secure=secure,
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    # Log errors using: app.logger.error('Some error message')
