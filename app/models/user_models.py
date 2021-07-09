# Copyright 2021 Simone Corti . All rights reserved

from flask_login import UserMixin, login_manager
# from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    return User.query.filter_by(id=user_id).first()

# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # The active flag is 1 for DEFAULT this way the user is created active
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    username = db.Column( db.String( 100, collation='NOCASE' ), nullable=False, unique=True )
    password = db.Column( db.String( 255 ), nullable=False, server_default='' )
    email = db.Column( db.String( 255 ), nullable=False, unique=True )
    email_confirmed_at = db.Column( db.DateTime() )

    # User information
    first_name = db.Column( db.String( 100, collation='NOCASE' ), nullable=False, server_default='' )
    last_name = db.Column( db.String( 100, collation='NOCASE' ), nullable=False, server_default='' )

    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))
    def has_role(self, role):
        for item in self.roles:
            if item.name == 'admin':
                return True
        return False

    def role(self):
        # print(self.roles)
        for item in self.roles:
            return item.name

    def name(self):
        # return str(self.full_name)
        return str( self.username )


# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes


class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), unique=True)
    data = db.Column(db.LargeBinary)
    expiry = db.Column(db.DateTime)


# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# Define the User registration form
# It augments the Flask-User RegisterForm with additional fields
# class MyRegisterForm(RegisterForm):
#     full_name = StringField('Full Name', validators=[validators.DataRequired('Full Name is required')])


# Define the User profile form
class UserProfileForm(FlaskForm):
    # full_name = StringField('Full Name', validators=[validators.DataRequired('Full Name is required')])
    # first_name = StringField('First Name', validators=[validators.DataRequired('First Name is required')])
    submit = SubmitField('Save')

# Define the Login form
class LoginForm(FlaskForm):
    # full_name = StringField('Full Name', validators=[validators.DataRequired('Full Name is required')])
    # first_name = StringField('First Name', validators=[validators.DataRequired('First Name is required')])
    submit = SubmitField('Save')
