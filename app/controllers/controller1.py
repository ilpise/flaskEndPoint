# Copyright 2021 Simone Corti. All rights reserved

from flask import Blueprint, redirect, render_template
from flask import request, url_for, flash, jsonify
from flask_login import login_user, current_user, logout_user

import logging

from app.models.user_models import User

import array
from .. import socketio

# Use of pyserial with conversion of HEX values to binary
# This fits better the command codes of COGES
# import serial
# import serial.tools.list_ports as port_list

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint('main', __name__, template_folder='templates')

@main_blueprint.route('/ping', methods=['GET'])
def ping():
    # socketio.emit('ping event', {'data': 42}, namespace='/chat')
    socketio.emit( 'my event', {'data': 42}, broadcast=True )
    return jsonify({"done" : "ok"})

@main_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.member_page'))


    # form = LoginForm(request.form)
    if request.method == 'POST':
        print('POST')
        print(request.get_json())


        # user = User.query.filter_by( username=request.form['username'] ).first()
        user = User.query.filter_by( username='admin' ).first()
        print(user)

        if user is None:
            flash('The user is not registered')
            return redirect(url_for('main.login'))

        login_user(user)
        logging.info('%s logged in successfully', user.username)
        # app.logger.info( '%s logged in successfully', user.username )
        flash('Logged in successfully.')
        return redirect(url_for('main.member_page'))

    return render_template('auth/login.html', title='Login',
                           # form=form
                           )

# @main_blueprint.route('/login', methods=['GET', 'POST'])
# def login():
#     # user = load_user(request.values.get('username'))
#     user = User.query.filter_by( username='admin' ).first()
#     print('api user: ', user)
#     if user :
#         login_user(user)
#         print( current_user )
#         return jsonify(status='ok', username=user.username)
#     else:
#         return jsonify(status='error', message='wrong username or hash')
#
# @main_blueprint.route("/login_screen", methods=['GET'])
# def login_screen():
#     print('login screen : ' , current_user)
#     if current_user.is_authenticated:
#         return redirect(url_for('main.member_page'))
#
#     return render_template('auth/login.html', title='Login')


@main_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))
    # return redirect( url_for( 'main.login_screen' ) )

# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/',
                      # methods=['GET', 'POST']
                      )
def member_page():
    print(current_user)
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))
        # return redirect( url_for( 'main.login_screen' ) )

    return render_template('views/controller1/member_base.html')

@main_blueprint.route('/coges')
def coges():
    if not current_user.is_authenticated:
        # return redirect(url_for('main.login'))
        return redirect( url_for( 'main.login_screen' ) )

    return render_template('views/controller1/testcoges.html')


@main_blueprint.route("/testsc")
def testsc():
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    # if not current_user.is_authenticated:
    #     return redirect(url_for('main.login'))

    r = readers()
    print( r )
    reader = r[0]
    print( "Sto usando: ", reader )
    connection = reader.createConnection()
    connection.connect()
    print( toHexString( connection.getATR() ) )

    # card responds with a dozen or more bytes of data known as the Answer To Reset (ATR).
    # This is usually a fixed sequence for any particular make and model of card,
    # and is intended to tell the reader / system some (limited) information about the card
    # and its capabilities, for example the maximum speed it can operate at, and its preferred voltage
    # and clock frequency.
    # After receiving the ATR, the reader, reader drivers and/or host software can then adjust various parameters
    # before getting stuck in with talking to the card

    # Seleziona del MF o Master Folder
    # All'interno dell'MF si trovano sia EF o Elementary File o file semplici sia DF o Directory File o sotto cartelle.
    # Il file che ci interessa si trova al seguente path: MF/DF1/EF_Dati_personali
    # CLS 00, istruzione A4 (seleziona file), P1 = P2 = 0 (seleziona per ID),
    # Lc: 2, Data: 3F00 (id del MF)
    SELECT_MF = [0x00, 0xA4, 0x00, 0x00, 0x02, 0x3F, 0x00]
    data, sw1, sw2 = connection.transmit( SELECT_MF )
    # se tutto è andato a buon fine sw1 e sw2 contengono
    # rispettivamente i valori 0x90 e 0x00 il corrispettivo del 200 in HTTP
    # print(data)
    print(sw1) # 144 = 0x90
    print(sw2) # 0

    # Seleziona del DF1...vedi sopra
    SELECT_DF1 = [0x00, 0xA4, 0x00, 0x00, 0x02, 0x11, 0x00]
    data, sw1, sw2 = connection.transmit( SELECT_DF1 )
    print(sw1) # 144 = 0x90
    print(sw2) # 0


    # Seleziona del file EF.Dati_personali... vedi sopra sopra
    SELECT_EF_PERS = [0x00, 0xA4, 0x00, 0x00, 0x02, 0x11, 0x02]
    data, sw1, sw2 = connection.transmit( SELECT_EF_PERS )
    print(sw1) # 144 = 0x90
    print(sw2) # 0

    # leggiamo i dati
    # CLS 00, istruzione B0 (leggi i dati binari contenuti nel file
    READ_BIN = [0x00, 0xB0, 0x00, 0x00, 0x00, 0x00]
    data, sw1, sw2 = connection.transmit( READ_BIN )
    # data contiene i dati anagrafici in formato binario
    # trasformiamo il tutto in una stringa
    # stringa_dati_personali = array.array('B', data).tostring()

    print(sw1) # 103 = 0x67 - https://github.com/LudovicRousseau/pyscard/blob/master/smartcard/sw/ISO7816_4ErrorChecker.py
    #  Wrong lenght in Lc
    # https://cardwerk.com/smart-card-standard-iso7816-4-section-5-basic-organizations/
    print(sw2) # 0

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
