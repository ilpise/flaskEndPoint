class ProductionConfig(object):
    DEBUG = False
    TESTING = False
    # Flask-WTF requires an enryption key - the string can be anything
    SECRET_KEY = 'some?bamboozle#string-foobar-pise$ishere'


class DevelopmentConfig(ProductionConfig):
    # DEBUG = True
    DEBUG = False
    TESTING = False

    # Flask settings
    CSRF_ENABLED = True

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/fep.sqlite'  # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning
    SESSION_TYPE = 'sqlalchemy'

    # Flask-User
    USER_PASSLIB_CRYPTCONTEXT_SCHEMES = ['bcrypt']
    USER_EMAIL_SENDER_EMAIL = 'thisPi@gmail.com'


    # OPENPLC
    # OPENPLC_IP = '172.17.0.4'
    OPENPLC_IP = '172.20.0.3'
    OPENPLC_MODBUS_PORT = 502

    # COGES
    COGES_PORT = '/dev/ttyACM0'
    COGES_BAUDRATE = 9600
    # NEBULAR_MERCHANT_ID = 'TODO'
    # NEBULAR_AUTH_TOKEN = 'TODO'

    # MQTT
    # MQTT_CLIENT_ID = 'flaskEP-vendor-test'
    MQTT_BROKER_URL = '85.94.200.117'
    MQTT_BROKER_PORT = 1883  # default port for non-tls connection
    # MQTT_USERNAME = ''  # set the username here if you need authentication for the broker
    # MQTT_PASSWORD = ''  # set the password here if the broker demands authentication
    MQTT_KEEPALIVE = 5  # set the time interval for sending a ping to the broker to 5 seconds
    MQTT_TLS_ENABLED = False  # set TLS to disabled for testing purposes

# class TestingConfig(ProductionConfig):
#     DEBUG = False
#     TESTING = True
