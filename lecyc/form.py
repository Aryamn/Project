from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField , TextAreaField,IntegerField
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
            
        
class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    time_slot = StringField('Time Slot',validators=[DataRequired()])
    features = TextAreaField('features')
    reg_no = StringField('Registration Number' , validators=[DataRequired()])
    #do image
    price = IntegerField('Price', validators=[DataRequired()])
    sell = BooleanField('sell')
    lend = BooleanField('lend')
    submit = SubmitField("Post")

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField(" Request Password Reset ")

    def validate_email(self,email):
            error = User.query.filter_by(email=email.data).first()

            if error is None:
                raise ValidationError("No account with that email . Please Register first")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class Ratings(FlaskForm):
    rating = IntegerField('Rating')
    submit = SubmitField('Update rating')