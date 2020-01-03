from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, DecimalField, TextAreaField, SubmitField,PasswordField, SelectField, BooleanField,RadioField
from wtforms.validators import DataRequired, Length, Optional, ValidationError, Email, EqualTo
from index.models import User


class Signup(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    age = StringField('Age', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    Faculty_name = StringField('Faculty', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField('Signup')


class Login(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=5, max=30)])
    passw = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')


class Posts(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=30)])
    name = StringField('Username', validators=[Length(min=5, max=30)])
    gender = StringField('Gender', validators=[DataRequired()])
    Faculty_name = StringField('Faculty', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    interest = TextAreaField('interests', validators=[DataRequired()])
    app_description = TextAreaField('interests', validators=[DataRequired()])
    submit = SubmitField('Post')


class UpdateAccount(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    age = StringField('Age', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    Faculty_name = StringField('Faculty', validators=[DataRequired()])
    picture = FileField('Update profile picture: ', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update?')

