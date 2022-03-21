from flask import flash
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError, InputRequired

from server.models import User


class ReferralForm(FlaskForm):
    code = StringField('Enter Promo code', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Activate')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(), Length(min=6, max=20), EqualTo('password')])
    country = StringField('Country', validators=[DataRequired(), Length(min=3, max=20)])
    referral = StringField('Referral')
    remember = BooleanField('Remember me')
    submit = SubmitField('Sing up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            flash("This username is taken. Please choose a different one")
            raise ValidationError("This username is taken. Please choose a different one")


    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        print(user)
        if user:
            flash("This email is taken. Please choose a different one")
            raise ValidationError("This email is taken. Please choose a different one")


class UserDataForm(FlaskForm):
    username = StringField()
    last_name = StringField()
    email = StringField()
    city = StringField()
    address = StringField()
    country = StringField()
    phone = StringField()
    state = StringField()
    zip = StringField()

    old_pass = PasswordField()

    password = PasswordField()
    submit = SubmitField('Submit')