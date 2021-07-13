import logging
import threading
import time
import random
import asyncio
from pymodbus.client.asynchronous.tcp import AsyncModbusTCPClient as ModbusClient
from pymodbus.client.asynchronous import schedulers
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

UNIT = 0x1


# Probabilmente questo è un worker
# vedi https://tutorialedge.net/python/concurrency/asyncio-event-loops-tutorial/
async def start_async_test(client):
    rr = await client.read_holding_registers( 1, 8, unit=UNIT )
    print( rr.registers )
    await asyncio.sleep(1)

# data_store = {'a': 1}
# def interval_query():
#     while True:
#         time.sleep( 5 )
#         vals = {'a': random.randint( 0, 100 )}
#         print( vals )
#         data_store.update( vals )

def test_modbus_thread():
    while True:
        print("---------------------RUN_WITH_NO_LOOP-----------------")
        loop, client = ModbusClient(schedulers.ASYNC_IO, port=5021)
        loop.run_until_complete(start_async_test(client.protocol))
        loop.close()
        print("--------DONE RUN_WITH_NO_LOOP-------------")

def create_app(config_class=DevelopmentConfig):

    # Asinc modbus stuff
    # run_with_no_loop()
    # Run with loop not yet started
    # run_with_not_running_loop()

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
    thread = threading.Thread( name='test_modbus_thread', target=test_modbus_thread )
    thread.setDaemon( True )
    thread.start()


    # logging.info( 'Started' )
    # Instantiate Flask
    app = Flask(__name__,
                static_folder='./freelancer',
                # static_folder='./oldStatic',
                # template_folder='./app/templates'
                )
    logging.basicConfig( filename='myapp.log', level=logging.INFO )
    # logger = logging.getLogger( __name__ )

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