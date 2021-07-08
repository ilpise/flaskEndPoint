class ProductionConfig(object):
    DEBUG = False
    TESTING = False
    # Flask-WTF requires an enryption key - the string can be anything
    SECRET_KEY = 'some?bamboozle#string-foobar-pise$ishere'


class DevelopmentConfig(ProductionConfig):
    DEBUG = True
    TESTING = False

    # Flask settings
    CSRF_ENABLED = True

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quickstart_app.sqlite'  # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning
    SESSION_TYPE = 'sqlalchemy'

    # Flask-User settings
    USER_APP_NAME = "Flask-User QuickStart App"  # Shown in and email templates and page footers
    # USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
    # USER_ENABLE_CHANGE_USERNAME = False  # Allow users to change their username
    # USER_ENABLE_CONFIRM_EMAIL = False  # Force users to confirm their email
    # USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords
    USER_ENABLE_EMAIL = False  # Register with Email
    # USER_EMAIL_SENDER_EMAIL = "noreply@example.com"
    # USER_ENABLE_REGISTRATION = True  # Allow new users to register
    USER_REQUIRE_RETYPE_PASSWORD = False  # Prompt for `retype password` in:
    USER_ENABLE_USERNAME = True  # Register and Login with username
    # USER_AFTER_LOGIN_ENDPOINT = 'main.member_page'
    # USER_AFTER_LOGOUT_ENDPOINT = 'main.member_page'
    # USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL = True
    # USER_LOGIN_URL = '/login' # Enable the portainer authentication



# class TestingConfig(ProductionConfig):
#     DEBUG = False
#     TESTING = True
