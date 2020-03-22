from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo ,ValidationError
from lecyc.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):

        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError("Username is taken . Please choose another")
            # print("Username is taken . Please choose another")

    def validate_email(self,email):

        error = User.query.filter_by(email=email.data).first()

        if error:
            raise ValidationError("Email is taken . Please choose another")
            # print("Username is taken . Please choose another")
            

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccount(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg' , 'png'])])

    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username :
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username is taken . Please choose another")
                # print("Username is taken . Please choose another")

    def validate_email(self,email):
        if email.data != current_user.email:
            error = User.query.filter_by(email=email.data).first()

            if error:
                raise ValidationError("Email is taken . Please choose another")
                # print("Username is taken . Please choose another")
            