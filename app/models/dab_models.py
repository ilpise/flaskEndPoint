# Copyright 2021 Simone Corti . All rights reserved

# from flask_user import UserMixin
# from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from app import db
from dataclasses import dataclass

# Define the Dab data model.
@dataclass
class Dab(db.Model):
    primary_key: int
    Name: str
    lat: str
    lon: str
    EdgeID: str
    PublicURL: str
    HumanName: str

    __tablename__ = 'dabs'
    primary_key = db.Column(db.Integer, primary_key=True)
    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    Name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    lat = db.Column(db.String(255), nullable=True, server_default='')
    lon = db.Column(db.String(255), nullable=True, server_default='')
    # edgekey = db.Column(db.String(255), nullable=True, unique=False, server_default='')
    EdgeID = db.Column( db.String( 255 ), nullable=False, unique=True, server_default='' )
    PublicURL = db.Column( db.String( 255 ), nullable=True)
    HumanName = db.Column( db.String( 255 ), nullable=True )


# Define the Dab edit form
class DabEditForm(FlaskForm):
    # full_name = StringField('Full Name', validators=[validators.DataRequired('Full Name is required')])
    # first_name = StringField('First Name', validators=[validators.DataRequired('First Name is required')])
    submit = SubmitField('Save')