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


# @main_blueprint.route("/settings")
# @login_required
# def settings():
#     pass
