# Copyright 2021 Simone Corti. All rights reserved

from flask import Blueprint, redirect, render_template, current_app, session
from flask import request, url_for, flash, send_from_directory, jsonify, render_template_string
from flask_user import current_user, login_required, roles_accepted
from flask_session import Session
from flask_login import login_user

from app import db
from app.models.user_models import LoginForm, UserProfileForm, User, UsersRoles, Role
from app.models.dab_models import Dab

import uuid, json, os
import datetime
import requests

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint('main', __name__, template_folder='templates')

@main_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    # print(form)

    if request.method == 'POST':
        # print('POST')
        # print( request.form )

        # Logic to get Bearer from Portainer
        res = requests.post('http://localhost:9000/api/auth',
                            json={"password": request.form['password'], "username": request.form['username']}
                           )
        if res.status_code == 200:
            print(res.json())
            session["port_auth_jwt"] = res.json()
            # t = session.get("test")
            user = User.query.filter( User.username == request.form['username'] ).first()
            if user:
                # print('user found')
                login_user( user )
                return redirect(url_for('main.member_page'))

    return render_template('flask_user/login.html', title='Login', form=form)



# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/',
                      # methods=['GET', 'POST']
                      )
def member_page():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))

    return render_template('views/controller1/member_base.html')


# Callback to get a json list of dabs - used for Leaflet map
@main_blueprint.route('/dabs')
@roles_accepted('admin', 'manager')  # Limits access to users with the 'admin' role
def dabs():
    dabs = Dab.query.all()
    return jsonify(dabs)

# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('views/admin/users.html')

@main_blueprint.route('/users')
@roles_accepted('admin')
def user_admin_page():
    users = User.query.all()
    return render_template('views/admin/users.html',
        users=users)

@main_blueprint.route('/create_or_edit_user', methods=['GET', 'POST'])
@roles_accepted('admin')
def create_or_edit_user_page():
    form = UserProfileForm(request.form, obj=current_user)
    roles = Role.query.all()
    user_id = request.args.get('user_id')
    user = User()
    user_roles = list()

    if user_id:
        user = User.query.filter(User.id == user_id).first()
        user_roles = user.roles

    if request.method == 'POST':
        if user.id is None:
            # user = User.query.filter(User.email == request.form['email']).first()
            user = User.query.filter(User.username == request.form['username']).first()
            if not user:
                user = User(email=request.form['email'],
                            username=request.form['username'],
                            first_name=request.form['first_name'],
                            last_name=request.form['last_name'],
                            password=current_app.user_manager.hash_password(request.form['password']),
                            active=True,
                            email_confirmed_at=datetime.datetime.utcnow())
                db.session.add(user)
                db.session.commit()
            return redirect(url_for('main.user_admin_page'))
        else:
            user.email = request.form['email']
            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            # print(request.form.getlist('role'))
            newroles = request.form.getlist('role')
            # Remove old roles if deselected
            for rol in user.roles:
                # print(rol.name)
                role = Role.query.filter( Role.name == str( rol.name ) ).first()
                # print(role)
                # print(user.roles)
                if rol.name not in newroles:
                    user.roles.remove(role)
                #     db.session.query( UsersRoles ).filter_by( user_id=user_id ).filter_by( role_id=role.id ).delete()
            # Add new roles if selected
            for rol in newroles:
                # print(rol)
                role = Role.query.filter( Role.name == str( rol ) ).first()
                user.roles.append(role)

            if request.form['password'] is not None and request.form['password'] is not "":
                user.password = current_app.user_manager.hash_password(request.form['password'])    
            db.session.commit()
            flash( 'User ' + user.name() + ' updated', 'success' )

    return render_template('views/admin/edit_user.html',
                           form=form,
                           roles=roles,
                           user_roles=user_roles,
                           user=user)

@main_blueprint.route('/manage_user_roles', methods=['GET', 'POST'])
@roles_accepted('admin')
def manage_user_roles():
    user_id = request.args.get('user_id')
    role_id = request.args.get('role_id')

    if user_id and role_id:
        user_id = int(user_id)
        role_id = int(role_id)
        db.session.query(UsersRoles).filter_by(user_id = user_id).filter_by(role_id = role_id).delete()
        db.session.commit()
    # Initialize form
    user_roles = list()
    if user_id is not None:
        user_id = int (user_id)
        user = User.query.filter_by(id=user_id).first()
        user_roles = user.roles

    form = UserProfileForm(request.form, obj=user)
    
    roles = db.session.query(Role).all()
    if request.method == 'POST':

        form.populate_obj(user) 
        if str(request.form['role']): 
            role = Role.query.filter(Role.name == str(request.form['role'])).first()
            user.roles.append(role)   
            db.session.commit()           
            flash('You successfully added a role to user '  + user.name() + ' !', 'success')  
        else:
            #user.roles = []  
            # print(f' Not appending role ') 
            flash('You failed to add a role to user '  + user.name() + ' !', 'failure')
            pass               
        
    return render_template('views/admin/manage_user_roles.html',
                            user=user,
                            roles=roles,
                            user_roles=user_roles,
                            form=form)

@main_blueprint.route('/delete_user', methods=['GET'])
@roles_accepted('admin')
def delete_user_page():
    try:
        user_id = request.args.get('user_id')

        db.session.query(UsersRoles).filter_by(user_id = user_id).delete()
        db.session.query(User).filter_by(id = user_id).delete()
        db.session.commit()

        flash('You successfully deleted your user!', 'success')
        return redirect(url_for('main.user_admin_page'))
    except Exception as e:
        flash('Opps!  Something unexpected happened.  On the brightside, we logged the error and will absolutely look at it and work to correct it, ASAP.', 'error')
        return redirect(request.referrer)

@main_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)
    print(current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        current_user.email = request.form['email']
        current_user.first_name = request.form['first_name']
        current_user.last_name = request.form['last_name']

        # print(current_user)
        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.user_profile_page'))

    # Process GET or invalid POST
    return render_template('views/controller1/user_profile_page.html',
                           current_user=current_user,
                           form=form)
