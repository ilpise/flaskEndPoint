# Copyright 2021 Simone Corti. All rights reserved

import logging
import asyncio
from flask import Blueprint, jsonify, current_app
# from flask_login import current_user
# import bcrypt
from flask_user import current_user, UserManager
# from app import user_manager
# from ..models.user_models import User
# from app import db, UserManager

from pymodbus.client.asynchronous.tcp import AsyncModbusTCPClient as ModbusClient
from pymodbus.client.asynchronous import schedulers
from pymodbus.client.sync import ModbusTcpClient

UNIT = 0x1


## Define a coroutine that takes in a future
async def myCoroutine():
    await asyncio.sleep( 1000 )
    print("My Coroutine")

## Define a coroutine that takes in a future
async def async_get_data(client):
    print('Enter async_get_data')
    print(client)
    if client is not None:
        rr = await client.read_holding_registers( 1, 8, unit=UNIT )
        # assert (not rr.isError())
        if not rr.isError():
            print( rr.registers )
            return rr.registers
    else:
        # uncomment to test concurrent requests
        # The modbus_server_machine1_1 must be stopped
        # await asyncio.sleep( 100 )
        return 'Error - check modbus server is reachable'

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
api_blueprint = Blueprint('api', __name__, template_folder='templates')

@api_blueprint.route('/modbus/api/testasync', methods=['GET'])
def read_modbus_async():
    new_loop, client = ModbusClient(schedulers.ASYNC_IO, port=5021)
    print ('C1')
    print(client)
    # assert(client is not None)
    results = new_loop.run_until_complete( async_get_data( client.protocol ) )
    new_loop.close()
    ret = {"sample return": results}
    return(jsonify(ret), 200)

@api_blueprint.route('/sample_api_request', methods=['GET'])
def sample_page():

    ret = {"sample return": 10}
    return(jsonify(ret), 200)


# Synchronous Client
@api_blueprint.route('/modbus/api/', methods=['GET'])
def read():
    OpenplcIp = current_app.config["OPENPLC_IP"]
    ModbusPort = current_app.config["OPENPLC_MODBUS_PORT"]

    # NOTE - the default port for modbus is 502
    client = ModbusTcpClient( OpenplcIp, port=ModbusPort )
    client.connect()

    rr = client.read_holding_registers( 1125, 1, unit=UNIT )

    assert (not rr.isError())
    print(rr)
    print(rr.registers)
    # logging.info( '%s logged in successfully', user.username )

    ret = {"response": rr.registers}
    return(jsonify(ret), 200)


# Check the pin inserted by the operator
@api_blueprint.route('/operator/checkpin', methods=['GET'])
def checkpin():

    if (current_app.user_manager.verify_password( '1234', current_user )):
        print('VALID USER')

    ret = {"response": "valid"}
    return(jsonify(ret), 200)
