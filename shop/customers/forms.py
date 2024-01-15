from wtforms import Form, IntegerField, DecimalField,StringField,SubmitField,PasswordField, BooleanField, TextAreaField, validators, ValidationError 
from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf import FlaskForm
from .model import Register


class CustomerRegisterForm(FlaskForm):
    name = StringField('Name', [validators.Length(min = 4, max = 25)])
    username = StringField('Username', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password:', [validators.DataRequired()])
    country = StringField('Country', [validators.Length(min = 4, max = 25)])
    state = StringField('State', [validators.Length(min = 4, max = 25)])
    city = StringField('City', [validators.Length(min = 4, max = 25)])
    contact = StringField('Contact', [validators.Length(min = 4, max = 25)])
    address = StringField('Address', [validators.Length(min = 4, max = 25)])
    zipcode = StringField('Zip code', [validators.Length(min = 4, max = 25)])

    profile = FileField('Profile', validators=[FileAllowed(['jpg','png','jpeg'], 'Image only')])

    submit = SubmitField('Register')

    def validate_username(self,username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")
        
    def validate_email(self,email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("This email is already in use!")
         
   


class CustomerLoginForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    

