from flask import flash
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError, InputRequired

from server.models import User, Post



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('amount', validators=[DataRequired()])
    submit = SubmitField('Continue')

class PostUpdateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Amount', validators=[DataRequired()])
    submit = SubmitField('Continue')