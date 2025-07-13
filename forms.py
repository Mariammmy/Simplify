from flask_wtf import FlaskForm
from wtforms.fields import (StringField, PasswordField, DateField, IntegerField, RadioField, SelectField, SubmitField, TextAreaField)

from wtforms.validators import DataRequired, length, equal_to, ValidationError
from flask_wtf.file import FileField, FileSize, FileAllowed, FileRequired

from models import User

class RegisterForm(FlaskForm):
    profile_image = FileField("Import profile picture", validators=[
        FileSize(1024 * 1024* 4),
        FileAllowed(["jpg", "jpeg", "png"])
    ])
    username = StringField("Enter username", validators=
                           [DataRequired()])
    password = PasswordField("Enter password", validators=
                            [DataRequired(), length(min=6, max=20)])
    confirm_password = PasswordField(validators=[DataRequired(), equal_to("password")])
    birthdate = DateField(validators=[DataRequired()])
    gender = RadioField("Choose gender", choices=["Female", "Male"], validators=[DataRequired()])
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken, Please choose another one.')

    register_button = SubmitField("Sign up")

class AddForm(FlaskForm):
    image = FileField("Import cover", validators=[
        FileSize(1024 * 1024* 4),
        FileAllowed(["jpg", "png", "jpeg"])
    ])
    heading = StringField("Name", validators=
                           [DataRequired()])
    category = SelectField('Category', choices=[
        ('', 'Category'),
        ('STEM', 'STEM'),
        ('Literature', 'Literature'),
        ('Art', 'Art'),
        ('Music', 'Music')
    ], validators=[DataRequired()])
    summary = TextAreaField("Summary", validators=
                           [DataRequired()])
    subheading1 = StringField("Subheading 1", validators=
                           [DataRequired()])
    text1 = TextAreaField("Paragraph 1", validators=
                        [DataRequired()])
    subheading2 = StringField("Subheading 2", validators=
                           [DataRequired()])
    text2 = TextAreaField("Paragraph 2", validators=
                        [DataRequired()])
    subheading3 = StringField("Subheading 3", validators=
                           [DataRequired()])
    text3 = TextAreaField("Paragraph 3", validators=
                        [DataRequired()])
    subheading4 = StringField("Subheading 4")
    text4 = TextAreaField("Paragraph 4")
    subheading5 = StringField("Subheading 5")
    text5 = TextAreaField("Paragraph 5")

    description = TextAreaField("Short description", validators=
                           [DataRequired(), length(min=20, max=100)])

    upload_button = SubmitField("Upload")

class CategoryForm(FlaskForm):
    image = FileField("Import cover", validators=[
        FileSize(1024 * 1024* 4),
        FileAllowed(["jpg", "png", "jpeg"])
    ])
    name = StringField("Name", validators=
                        [DataRequired()])
    description = StringField("Description", validators=
                        [DataRequired()])
    link = StringField("Link to page", validators=
                        [DataRequired()])
    upload_button = SubmitField("Upload")


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    login_button = SubmitField("Log in") 

class FeedbackForm(FlaskForm):
    headline = StringField("Headline", validators=
                           [DataRequired()])
    message = TextAreaField("Message", validators=
                           [DataRequired()])
    submit_button = SubmitField("Submit")
