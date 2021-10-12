import logging
import threading
import time
import random
import asyncio

# MODBUS on TCP async
from pymodbus.client.asynchronous.tcp import AsyncModbusTCPClient as ModbusClient
# MODBUS on serial port async
# from pymodbus.client.asynchronous.serial import (AsyncModbusSerialClient as ModbusClient)

from pymodbus.client.asynchronous import schedulers
from flask import Flask
# from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_login import LoginManager
# from flask_user import UserManager
from config import DevelopmentConfig
from flask_mqtt import Mqtt

# Instantiate Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf_protect = CSRFProtect()
migrate = Migrate()
mqtt = Mqtt()

UNIT = 0x1


# a simple card observer that prints inserted/removed cards
# class PrintObserver(CardObserver):
#     """A simple card observer that is notified
#     when cards are inserted/removed from the system and
#     prints the list of cards
#     """
#
#     def update(self, observable, actions):
#         (addedcards, removedcards) = actions
#         for card in addedcards:
#             print("+Inserted: ", toHexString(card.atr))
#             # user = User.query.filter_by( username='admin' ).first()
#         for card in removedcards:
#             print("-Removed: ", toHexString(card.atr))

# Define a coroutine that takes in a future
# vedi https://tutorialedge.net/python/concurrency/asyncio-event-loops-tutorial/


async def start_async_test(client):
    rr = await client.read_holding_registers( 1, 8, unit=UNIT )
    print( rr.registers )
    await asyncio.sleep( 1 )


# data_store = {'a': 1}
# def interval_query():
#     while True:
#         time.sleep( 5 )
#         vals = {'a': random.randint( 0, 100 )}
#         print( vals )
#         data_store.update( vals )


def test_modbus_thread():
    while True:
        print( "---------------------RUN_WITH_NO_LOOP-----------------" )
        loop, client = ModbusClient( schedulers.ASYNC_IO, port=5021 )
        loop.run_until_complete( start_async_test( client.protocol ) )
        loop.close()
        print( "--------DONE RUN_WITH_NO_LOOP-------------" )


# def smart_card_thread():
#     while True:
#         print("---------------------RUN_WITH_NO_LOOP-----------------")
#         loop, client = ModbusClient(schedulers.ASYNC_IO, port=5021)
#         loop.run_until_complete(start_async_test(client.protocol))
#         loop.close()
#         print("--------DONE RUN_WITH_NO_LOOP-------------")


def create_app(config_class=DevelopmentConfig):
    # https://stackoverflow.com/questions/36342718/starting-background-daemon-in-flask-app
    # Test using threading
    # Questo funziona - se lanciamo l'applicazione vengono printati i vals nel log
    # e l'applicazione web funziona contemporaneamente
    # data_store = {'a': 1}
    # def interval_query():
    #     while True:
    #         time.sleep( 5 )
    #         vals = {'a': random.randint( 0, 100 )}
    #         print(vals)
    #         data_store.update( vals )

    # thread = threading.Thread( name='interval_query', target=interval_query )

    # UNCOMMENT TO HAVE MODBUS DAEMON
    # thread = threading.Thread( name='test_modbus_thread', target=test_modbus_thread )
    # thread.setDaemon( True )
    # thread.start()

    # logging.info( 'Started' )
    # Instantiate Flask
    app = Flask( __name__,
                 static_folder='./freelancer',
                 # static_folder='./oldStatic',
                 # template_folder='./app/templates'
                 )
    # logging.basicConfig( filename='myapp.log', level=logging.INFO )
    # logger = logging.getLogger( __name__ )

    app.config.from_object( config_class )
    # Database to use flask db
    # Setup Flask-SQLAlchemy
    db.init_app( app )
    # Setup Flask-Migrate
    migrate.init_app( app, db )
    # Setup session
    Session( app )
    # Setup WTForms CSRFProtect
    csrf_protect.init_app( app )
    # Setup mqtt client
    mqtt.init_app( app )

    # # Set default subscriptions
    # @mqtt.on_connect()
    # def handle_connect(client, userdata, flags, rc):
    #     mqtt.subscribe('vendors/create_update')
    #
    # @mqtt.on_message()
    # def handle_mqtt_message(client, userdata, message):
    #     data = dict(
    #         topic=message.topic,
    #         payload=message.payload.decode()
    #     )
    #     print( data )

    from app.controllers.mqtt import handle_connect
    from app.controllers.mqtt import handle_mqtt_message

    from app.controllers.controller1 import main_blueprint
    from app.controllers.apis import api_blueprint
    from app.controllers.apicoges import apicoges_blueprint
    # from app.controllers.controller2 import controller2_blueprint
    app.register_blueprint( main_blueprint )
    app.register_blueprint( api_blueprint )
    app.register_blueprint( apicoges_blueprint )
    # app.register_blueprint(controller2_blueprint)
    csrf_protect.exempt( main_blueprint )
    csrf_protect.exempt( api_blueprint )
    csrf_protect.exempt( apicoges_blueprint )

    login_manager.init_app( app )

    # Flask-User integration
    # from .models.user_models import User
    # user_manager = UserManager( app, db, User )

    return app
