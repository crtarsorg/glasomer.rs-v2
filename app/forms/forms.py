#coding=utf-8
from flask_wtf import FlaskForm
from wtforms import TextAreaField, RadioField, TextField, SelectField, SelectMultipleField, BooleanField, PasswordField
from wtforms.validators import Email, DataRequired


class LoginForm(FlaskForm):
    email = TextField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


