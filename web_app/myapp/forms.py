from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeLocalField, DateTimeField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import Length, DataRequired, EqualTo, Email, ValidationError
from flask_wtf.file import FileRequired, FileField
from myapp.model import User
from flask_babel import lazy_gettext as _1


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError(
                "Username already exists! Please try a different usename"
            )
        
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()

        if email_address is not None:
            raise ValidationError('Email address already exists! Please try a different email')
        
    def validate_max_admins(form, field):
        if field.data == 'admin':
            admin_count = User.query.filter_by(role='admin').count()
            if admin_count >= 2:  # Change 2 to your desired maximum number of admins
                raise ValidationError('The maximum number of admin users has been reached.')
    username = StringField(label='Your Name', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Your Email', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    user_count = IntegerField(label='User count')
    confirm_password = PasswordField(label='Confirm Password:', validators=[EqualTo('password'), DataRequired()])
    role = SelectField(label='Your Role', choices=[('admin', 'Admin'), ('editor', 'Editor'), ('writer', 'Writer'), ('student', 'Student')], validators=[DataRequired()])
    submit = SubmitField(label='Create Account')
    
    
    
    
    
class LoginForm(FlaskForm):
    email_address = StringField(label='Your Email', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember me')
    submit = SubmitField(label='Login')

class AssignmentForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])
    subject = StringField(label='Subject', validators=[DataRequired()])
    description = TextAreaField(label='Asignment description', validators=[Length(min=0, max=1000), DataRequired()])
    word_count = IntegerField(label='Word count', validators=[DataRequired()])
    pages = IntegerField(label='Pages', validators=[DataRequired()])
    assignment_type = StringField(label='Assignment type', validators=[DataRequired()])
    academic_level = StringField(label='Academic level', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    order_id = StringField(label='Order id', validators=[DataRequired()])
    deadline = DateTimeLocalField(label='Deadline', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField(label='Post')


class PostAsignmentForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])
    subject = StringField(label='Subject', validators=[DataRequired()])
    description = TextAreaField(label='Asignment description', validators=[Length(min=0, max=1000), DataRequired()])
    word_count = IntegerField(label='Word count', validators=[DataRequired()])
    assignment_type = StringField(label='Assignment type', validators=[DataRequired()])
    academic_level = StringField(label='Academic level', validators=[DataRequired()])
    deadline = DateTimeLocalField(label='Deadline', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField(label='Post')

class EditAsignment(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    deadline = StringField('Deadline', validators=[DataRequired()])
    Asignment_description = TextAreaField('Asignment Description', validators=[Length(min=0, max=1000), DataRequired()])
    pricing = StringField('Price', validators=[DataRequired()])
    submit = SubmitField(label='Submit Changes')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class TakeOrder(FlaskForm):
    submit = SubmitField(label='Take Order!')

class UpdateOrder(FlaskForm):
    submit = SubmitField(label='Update Assignment!')

class DeleteOrder(FlaskForm):
    submit = SubmitField(label='Delete Assignment!')

class DeclineOrder(FlaskForm):
    submit = SubmitField(label='Decline Order!')

    