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


# class TestingConfig(ProductionConfig):
#     DEBUG = False
#     TESTING = True
