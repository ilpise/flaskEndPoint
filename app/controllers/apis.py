# Copyright 2021 Simone Corti. All rights reserved

import logging
import asyncio
from flask import Blueprint, redirect, render_template
from flask import request, url_for, flash, send_from_directory, jsonify, render_template_string
# from flask_user import current_user, login_required, roles_accepted

from app import db
from app.models.user_models import UserProfileForm
import uuid, json, os
import datetime

from pymodbus.client.sync import ModbusTcpClient

UNIT = 0x1


async def async_get_data(client):
    rr = await client.read_holding_registers( 1, 8, unit=UNIT )
    print(rr.refisters)
    await asyncio.sleep(1)
    return 'Done!'

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
api_blueprint = Blueprint('api', __name__, template_folder='templates')

@api_blueprint.route('/sample_api_request', methods=['GET'])
def sample_page():

    ret = {"sample return": 10}
    return(jsonify(ret), 200)


@api_blueprint.route('/modbus/api/', methods=['GET'])
def read():

    # NOTE - the default port for modbus is 502 o 5020?? but the server we implemented run on 5021
    client = ModbusTcpClient( 'localhost', port=5021 )
    client.connect()
    # logging.info( '%s logged in successfully', user.username )

    rr = client.read_holding_registers( 0, 8, unit=UNIT )
    assert (not rr.isError())
    print(rr)
    print(rr.registers)
    # logging.info( '%s logged in successfully', user.username )

    ret = {"sample return": 10}
    return(jsonify(ret), 200)


# NOTE: this route does NOT works
# Install Flask with the 'async' extra in order to use async views.
@api_blueprint.route('/modbus/api/testasync', methods=['GET'])
async def read_modbus_async():
    data = await async_get_data()
    return data