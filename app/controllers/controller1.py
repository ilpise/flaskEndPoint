# Copyright 2021 Simone Corti. All rights reserved
import json

from flask import Blueprint, redirect, render_template
from flask import request, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user
# from flask_user import current_user
import logging

from app import db, mqtt
from app.models.user_models import User, Role

import array


# Use of pyserial with conversion of HEX values to binary
# This fits better the command codes of COGES
# import serial
# import serial.tools.list_ports as port_list

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint('main', __name__, template_folder='templates')

@main_blueprint.route("/splash_screen", methods=['GET'])
def splash_screen():
    print('login screen : ' , current_user)
    if current_user.is_authenticated:
        return redirect(url_for('main.member_page'))

    return render_template('views/controller1/splash.html',
                           title='Welcome')


@main_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.member_page'))

    # form = LoginForm(request.form)
    if request.method == 'GET':
        print('GET')

        # The username or C.F. is passed from the optic reader
        username = request.args.get( 'username' )
        user = User.query.filter_by( username=username ).first()

        if user is None:
            # The user is not registered
            print('NONE')
            # TODO Register the user
            # Get the customer role
            role = Role.query.filter( Role.name == str( 'customer' ) ).first()
            # Create the user - without mail
            user = User( username=username,
                         password='plaintextpassword',
                         active=True,
                         credit=0)
            if role:
                user.roles.append( role )
            db.session.add( user )
            db.session.commit()

            # Authenticate the user
            login_user( user )
            # Redirect to insert mail page
            return redirect( url_for( 'main.mail_page' ) )
        else :
            user_roles_names = [role.name for role in user.roles]
            print( user_roles_names )
            if user.has_role('admin'):
                print('Admin')
            if user.has_role('manager'):
                print('Manager')
            if user.has_role('operator'):
                print('Operatore')
            if user.has_role('customer'):
                print('CUstomer')

            login_user(user)
            logging.info('%s logged in successfully', user.username)
            # app.logger.info( '%s logged in successfully', user.username )
            flash('Logged in successfully.')
            return redirect(url_for('main.member_page'))

    return render_template('auth/login.html',
                           title='Login'
                           )
    # return render_template('views/controller1/email_base.html',
    #                        title='Login'
    #                        )

@main_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.splash_screen'))
    # return redirect( url_for( 'main.login_screen' ) )

# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/')
def member_page():
    print('controller1 current_user ', current_user)
    user_roles_names = [role.name for role in current_user.roles]
    print( current_user.id, current_user.username, current_user.email, user_roles_names)

    objuser = {'gid': 1,
               'id':current_user.id,
               'username':current_user.username,
               'email':current_user.email,
               'roles':user_roles_names,
               'credit':0}
    jsonuser = json.dumps(objuser)
    mqtt.publish( 'user/create', jsonuser )

    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))
        # return redirect( url_for( 'main.login_screen' ) )

    if current_user.has_role('operator'):
        return render_template('views/controller1/operator.html',
                               user_name=current_user.username)

    return render_template('views/controller1/member_base.html',
                           credit_residuo=current_user.credit)

# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/insert_mail',  methods=['GET', 'POST'])
def mail_page():
    # print('CURRENT USER')
    # print(current_user)
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        email = request.form['email']
        if email:
            current_user.email = email
            db.session.commit()

        print('NEW - EMAIL')
        print(current_user)
        # Publish the user creation to create the user in drupal
        # jsonstring = jsonify(current_user)
        # mqtt.publish('user/create', current_user)

        return redirect( url_for( 'main.member_page' ) )

    return render_template('views/controller1/email_base.html')

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
    # se tutto ?? andato a buon fine sw1 e sw2 contengono
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
