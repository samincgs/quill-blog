from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField, TextAreaField
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
    
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Post Content', validators=[DataRequired()], render_kw={'rows': 7, 'cols': 4})
    submit = SubmitField('Post')
           
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    image = FileField('Upload a new Profile Picture', validators=[FileAllowed(upload_set=['png', 'jpg'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username): # checks if a user already exists with this username & updates username
        if current_user.username != username.data: # only do if the user is not inputting the same credentials
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists! Please choose a different one.')
        
    def validate_email(self, email): # checks if a user already exists with this email
        if current_user.email != email.data: # only do if the user is not inputting the same credentials
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists! Please choose a different one.')
            
            