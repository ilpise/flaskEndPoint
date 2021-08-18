# Copyright 2021 Simone Corti. All rights reserved

# import app
from flask import Blueprint, redirect, render_template, current_app, session
from flask import request, url_for, flash, send_from_directory, jsonify, render_template_string
from flask_session import Session
from flask_login import login_user, current_user, logout_user

import logging
from app.models.user_models import LoginForm, User
from app.models.dab_models import Dab

import uuid, json, os
import datetime
import requests

# Smartcard
from smartcard.System import readers
import array


# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint('main', __name__, template_folder='templates')


@main_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.member_page'))

    form = LoginForm(request.form)
    if request.method == 'POST':
        user = User.query.filter_by( username=request.form['username'] ).first()
        print(user)

        if user is None:
            flash('The user is not registered')
            return redirect(url_for('main.login'))

        login_user(user)
        logging.info('%s logged in successfully', user.username)
        # app.logger.info( '%s logged in successfully', user.username )
        flash('Logged in successfully.')
        return redirect(url_for('main.member_page'))

    return render_template('auth/login.html', title='Login', form=form)

@main_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/',
                      # methods=['GET', 'POST']
                      )
def member_page():
    print(current_user)
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))

    return render_template('views/controller1/member_base.html')


@main_blueprint.route("/testsc")
def testsc():
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))

    r = readers()
    print( r )
    reader = r[0]
    print( "Sto usando: ", reader )
    connection = reader.createConnection()
    connection.connect()
    # Seleziona del MF
    # CLS 00, istruzione A4 (seleziona file), P1 = P2 = 0 (seleziona per ID),
    # Lc: 2, Data: 3F00 (id del MF)
    SELECT_MF = [0x00, 0xA4, 0x00, 0x00, 0x02, 0x3F, 0x00]
    data, sw1, sw2 = connection.transmit( SELECT_MF )
    # se tutto è andato a buon fine sw1 e sw2 contengono
    # rispettivamente i valori 0x90 e 0x00 il corrispettivo del 200 in HTTP

    # Seleziona del DF1...vedi sopra
    SELECT_DF1 = [0x00, 0xA4, 0x00, 0x00, 0x02, 0x11, 0x00]
    data, sw1, sw2 = connection.transmit( SELECT_DF1 )

    # Seleziona del file EF.Dati_personali... vedi sopra sopra
    SELECT_EF_PERS = [0x00, 0xA4, 0x00, 0x00, 0x02, 0x11, 0x02]
    data, sw1, sw2 = connection.transmit( SELECT_EF_PERS )

    # leggiamo i dati
    # CLS 00, istruzione B0 (leggi i dati binari contenuti nel file
    READ_BIN = [0x00, 0xB0, 0x00, 0x00, 0x00, 0x00]
    data, sw1, sw2 = connection.transmit( READ_BIN )
    # data contiene i dati anagrafici in formato binario
    # trasformiamo il tutto in una stringa
    # stringa_dati_personali = array.array('B', data).tostring()
    stringa_dati_personali = array.array( 'B', data ).tobytes()

    prox_field_size = int( stringa_dati_personali[6:8], 16 )
    da = 8
    a = da + prox_field_size
    if prox_field_size > 0:
        codice_emettitore = stringa_dati_personali[da:a]
        print( "Codice emettitore: ", codice_emettitore.decode( "utf-8" ) )

    da = a
    a += 2
    prox_field_size = int( stringa_dati_personali[da:a], 16 )
    da = a
    a += prox_field_size
    if prox_field_size > 0:
        data_rilascio_tessera = stringa_dati_personali[da:a]
        print( "Data rilascio tessera: ",
               data_rilascio_tessera[0:2].decode( "utf-8" ) + "/" + data_rilascio_tessera[2:4].decode(
                   "utf-8" ) + "/" + data_rilascio_tessera[-4:].decode( "utf-8" ) )

    da = a
    a += 2
    prox_field_size = int( stringa_dati_personali[da:a].decode( "utf-8" ), 16 )
    da = a
    a += prox_field_size
    if prox_field_size > 0:
        data_scadenza_tessera = stringa_dati_personali[da:a]
        print( "Data scadenza tessera: ",
               data_scadenza_tessera[0:2].decode( "utf-8" ) + "/" + data_scadenza_tessera[2:4].decode(
                   "utf-8" ) + "/" + data_scadenza_tessera[-4:].decode( "utf-8" ) )

    da = a
    a += 2
    prox_field_size = int( stringa_dati_personali[da:a].decode( "utf-8" ), 16 )
    da = a
    a += prox_field_size
    if prox_field_size > 0:
        cognome = stringa_dati_personali[da:a].decode( "utf-8" )
        print( "Cognome: ", cognome )

    return render_template( 'views/controller1/testsc.html',
                            cognome=cognome)

@main_blueprint.route("/testcoges")
def testcoges():
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))

    # Use of pyserial with conversion of HEX values to binary
    # This fits better the command codes of COGES

    import serial
    import serial.tools.list_ports as port_list

    ports = list(port_list.comports())
    print(ports[0].device)
    port = ports[0].device
    baudrate = 9600
    serialPort = serial.Serial(port=port, baudrate=baudrate,
                                    bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE)
    serialString = ""


    # COGES PARTS
    start = '{'
    stop = '}'

    slave_address = '1'
    command_code = '20' # a1

    # Calculate the checksum
    a = format(ord(slave_address), "x") # 31
    checksum = hex(int(a, 16) + int(command_code, 16))
    # remove the 0x before the number and fill an array
    # print(checksum[2:])
    checkarr = list(checksum[2:])
    # print(checkarr)
    # print(format(ord(checkarr[0]), "x"))
    # Compose the command
    fullcommand = format(ord(start), "x")+a+str(command_code)+format(ord(stop), "x")+format(ord(checkarr[0]), "x")+format(ord(checkarr[1]), "x")
    # print(fullcommand.upper())
    serialPort.write(bytes.fromhex(fullcommand))

    line = serialPort.readline()
    # print( line )

    serialPort.close()

    return render_template( 'views/controller1/testcoges.html',
                            line=line)