from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, SelectField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError, InputRequired

OPTIONS = ['other', 'deposit', 'withdraw', 'trade balance', 'report']


class SupportForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    category = SelectField(validators=[DataRequired()], choices=OPTIONS)
    topic = StringField(validators=[DataRequired()])
    text = StringField(validators=[DataRequired(), Length(min=3, max=100)])
    submit = SubmitField('Send')


class CommentsForm(FlaskForm):
    text = TextAreaField(validators=[DataRequired(), Length(min=3, max=300)])
    submit = SubmitField('Send')
