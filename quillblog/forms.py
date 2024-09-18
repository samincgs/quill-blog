from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from quillblog.models import User

class RegistrationForm(FlaskForm): # inherits from flaskform
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) 
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    # custom validation methods that start with validate_(field)
    def validate_username(self, username): # checks if a user has already registed with a certain username
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists! Please choose a different one.')
        
    def validate_email(self, email): # checks if a user has already registed with a certain email
        user_email = User.query.filter_by(email=email.data).first()
        if user_email:
            raise ValidationError('Email already exists! Please choose a different one.')
    
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')