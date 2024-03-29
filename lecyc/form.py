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
                                    
    name = StringField('Name',validators=[DataRequired()])
    roll_no = StringField('Roll No.',validators=[DataRequired()])
    hall = StringField('Hall Name',validators=[DataRequired()])
    mobile_no = StringField('Mobile No.',validators=[DataRequired()])

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

    def validate_roll_no(self,roll_no):
       
        error = User.query.filter_by(roll_no=roll_no.data).first()

        if error:
            raise ValidationError("Roll number is taken . Please check it carefully")

    def validate_mobile_no(self,mobile_no):
        error = User.query.filter_by(mobile_no=mobile_no.data).first()

        if error:
            raise ValidationError("Mobile number is taken . Please check it carefully")
            

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
    
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg' , 'png','jpeg'])])

    submit = SubmitField('Update')

    name = StringField('Name',validators=[DataRequired()])
    roll_no = StringField('Roll No.',validators=[DataRequired()])
    hall = StringField('Hall Name',validators=[DataRequired()])
    mobile_no = StringField('Mobile No.',validators=[DataRequired()])

    def validate_username(self,username):
        if username.data != current_user.username :
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username is taken . Please choose another")
               

    def validate_email(self,email):
        if email.data != current_user.email:
            error = User.query.filter_by(email=email.data).first()

            if error:
                raise ValidationError("Email is taken . Please choose another")

    def validate_roll_no(self,roll_no):
        if roll_no.data != current_user.roll_no:
            error = User.query.filter_by(roll_no=roll_no.data).first()

            if error:
                raise ValidationError("Roll number is taken . Please check it carefully")

    # def validate_mobile_no(self,mobile_no):
    #     if mobile_no.data != current_user.mobile_no:
    #         error = User.query.filter_by(mobile_no=mobile_no.data).first()

    #         if error:
    #             raise ValidationError("Mobile number is taken . Please check it carefully")
                
            
        
class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    time_slot_start = IntegerField('Start Time',validators=[DataRequired()])
    time_slot_end = IntegerField('End Time',validators=[DataRequired()])

    time_slot_meri_start = StringField('Meridian',validators=[DataRequired()],render_kw={"placeholder":"am"})

    time_slot_meri_end = StringField('Meridian',validators=[DataRequired()],render_kw={"placeholder":"am"})

    date_avail = IntegerField('Date',validators=[DataRequired()],render_kw={"placeholder":"20"})

    month_avail = IntegerField('Month',validators=[DataRequired()],render_kw={"placeholder":"1"})

    features = TextAreaField('features')
    reg_no = StringField('Registration Number' , validators=[DataRequired()])
    image = FileField('Upload Cycle picture', validators=[FileAllowed(['jpg','png','jpeg'])])
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

class Search(FlaskForm):
    time = IntegerField('start_time',render_kw={"placeholder":"Enter time Eg:2"})
    submit = SubmitField('Search')

class Commenting(FlaskForm):
    comment = TextAreaField('comment', validators=[DataRequired()])
    submit = SubmitField('Post')