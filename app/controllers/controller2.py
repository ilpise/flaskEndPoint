# Copyright 2021 Simone Corti. All rights reserved

from flask import Blueprint, redirect, render_template, session
from flask import request, url_for, flash, send_from_directory, jsonify, render_template_string
from flask_user import current_user, login_required, roles_accepted
import requests
import json

from app import db
from app.models.dab_models import Dab, DabEditForm

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
controller2_blueprint = Blueprint( 'controller2', __name__, template_folder='templates' )


@controller2_blueprint.route( '/example', methods=['GET'] )
def sample_page():
    return render_template( 'views/controller2/example.html' )


@controller2_blueprint.route( '/dab_list', methods=['GET'] )
@roles_accepted( 'admin', 'manager' )
def dab_list():
    # Query database
    dabs = Dab.query.all()
    # print( type( dabs ) )


    # Get the portainer endpoints associated with the auth user
    jwt = session.get( "port_auth_jwt" )
    # print(jwt)
    if jwt is not None:
        headers_dict = {"Authorization": "Bearer " + jwt['jwt']}
        user_endpoints = requests.get( 'http://localhost:9000/api/endpoints',
                                       headers=headers_dict )
        if user_endpoints.status_code == 200:
            # print(type(user_endpoints))
            ue_json = user_endpoints.json()
            print(ue_json)

            for endpoint in ue_json:
                # print( endpoint['EdgeID'] )
                if endpoint['Id'] != 1 :
                    stored = Dab.query.filter_by( EdgeID=endpoint['EdgeID'] ).first()
                    if not stored:
                        new = Dab(Name=endpoint['Name'], EdgeID=endpoint['EdgeID'], PublicURL=endpoint['PublicURL'])
                        db.session.add( new )
                        db.session.commit()

                # dabs.append( endpoint )

    # # Attach endpoints to dabs
    # for dab in dabs:
    #     print( dab )

    return render_template( 'views/controller2/dab_list.html',
                            dabs=dabs )


@controller2_blueprint.route( '/dab', methods=['GET'] )
@roles_accepted( 'admin', 'manager' )
def dab():
    dab_id = request.args.get( 'dab_id' )
    dab = Dab()

    if dab_id:
        dab = Dab.query.filter( Dab.primary_key == dab_id ).first()

    return render_template( 'views/controller2/dab.html',
                            dab=dab )

@controller2_blueprint.route( '/edit_dab', methods=['GET', 'POST'] )
@roles_accepted( 'admin', 'manager' )
def edit_dab():
    form = DabEditForm( request.form, obj=current_user )
    dab_id = request.args.get( 'dab_id' )
    dab = Dab()

    if dab_id:
        dab = Dab.query.filter( Dab.primary_key == dab_id ).first()

    if request.method == "POST":
        try:
            Dab.query.filter_by( primary_key=dab_id ).update( dict( HumanName=request.form['humanname'] ) )
            db.session.commit()
            flash( 'Dab updated', 'success' )
        except Exception as e:
            # print( e )
            flash( 'Failed to update Dab', 'error' )

    return render_template( 'views/controller2/edit_dab.html',
                            form=form,
                            dab=dab )

@controller2_blueprint.route('/setlatlng', methods=['GET','POST'])
@roles_accepted('admin', 'manager')  # Limits access to users with the roles
def setlatlng():
    if request.method == "POST":
        # print(request.json['dabId'])
        # print(request.get_json())
        try:
            Dab.query.filter_by( primary_key=request.json['dabId'] ).update( dict( lat=request.json['lat'], lon=request.json['lng'] ) )
            db.session.commit()
            # flash( 'Marker position updated', 'success' )
            msg = {"msg": "Marker updated successfully",
                   # "data": updateddata.serializers()
                   }
        except Exception as e:
            # print( e )
            # flash( 'Failed to update marker position', 'error' )
            msg = {"msg": "Failed to update map marker."}
            # code = 500
        return msg


@controller2_blueprint.route( '/test_ext_request', methods=['GET'] )
@roles_accepted( 'admin', 'manager' )
def test_ext_request():
    is_dict = session.get( "port_auth_jwt" )
    headers_dict = {"Authorization": "Bearer " + is_dict['jwt']}
    user_endpoints = requests.get( 'http://localhost:9000/api/endpoints',
                                   headers=headers_dict )

    if user_endpoints.status_code == 200:
        # print(type(user_endpoints))
        ue_json = user_endpoints.json()
        for endpoint in ue_json:
            print( endpoint['Id'] )
        # print(user_endpoints.json())

    return render_template( 'views/controller2/ext_resp.html',
                            response=user_endpoints.json(),
                            )
