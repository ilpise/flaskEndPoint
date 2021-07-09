
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_login import LoginManager
from config import DevelopmentConfig

# Instantiate Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf_protect = CSRFProtect()
migrate = Migrate()

def create_app(config_class=DevelopmentConfig):
    # Instantiate Flask
    app = Flask(__name__,
                static_folder='./freelancer',
                # static_folder='./oldStatic',
                # template_folder='./app/templates'
                )

    app.config.from_object(config_class)
    # Database to use flask db
    # Setup Flask-SQLAlchemy
    db.init_app(app)
    # Setup Flask-Migrate
    migrate.init_app(app, db)
    # Setup session
    Session(app)
    # Setup WTForms CSRFProtect
    csrf_protect.init_app(app)

    from app.controllers.controller1 import main_blueprint
    from app.controllers.apis import api_blueprint
    # from app.controllers.controller2 import controller2_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint)
    # app.register_blueprint(controller2_blueprint)
    csrf_protect.exempt(api_blueprint)

    login_manager.init_app(app)

    return app