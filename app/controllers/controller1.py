# Copyright 2021 Simone Corti. All rights reserved

from flask import Blueprint, redirect, render_template, current_app, session
from flask import request, url_for, flash, send_from_directory, jsonify, render_template_string
# from flask_user import current_user, login_required, roles_accepted
from flask_session import Session
from flask_login import login_user, current_user, login_required


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
        return redirect( url_for( 'index' ) )

    form = LoginForm(request.form)
    # print(form)

    if request.method == 'POST':
        user = User.query.filter_by( username=request.form['username'] ).first()
        print(user)
        login_user(user)
        flash('Logged in successfully.')

    return render_template('flask_user/login.html', title='Login', form=form)



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
