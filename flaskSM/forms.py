from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields.simple import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flaskSM.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                            Length(min=3, max=10)],render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})
    password2 = PasswordField('Confim password', validators=[DataRequired(),
                            EqualTo('password')], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()],render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[Length(max=20)])
    content = TextAreaField('Content', validators=[Length(max=30000)])
    file = FileField('File', validators=[FileAllowed(['jpeg', 'png'], 'Images only!')])
    submit = SubmitField('Add post')

class EditPostForm(FlaskForm):
    title = StringField('Title', validators=[Length(max=20)])
    content = TextAreaField('Content', validators=[Length(max=30000)])
    file = FileField('File', validators=[FileAllowed(['jpeg', 'png'], 'Images only!')])
    submit = SubmitField('Save')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                        Length(min=3, max=10)], render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Email"})
    bio = TextAreaField('Bio',validators=[Length(max=225)], render_kw={"placeholder": "About yourself"})
    file = FileField('File', validators=[FileAllowed(['jpeg', 'png'], 'Images only!')])
    submit = SubmitField('Save')