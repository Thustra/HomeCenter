from flask_wtf import Form
from wtforms import StringField, PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class LoginForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )

class RegistrationForm(Form):
    username = StringField(
        'username',
        validators=[
            DataRequired(),
            Length(min=3,max=25)
        ]
    )
    email = StringField(
        'email',
        validators=[
            DataRequired(),
            Email(message=None),
            Length(min=3,max=40)
        ]
    )
    password = PasswordField(
        'password',
        validators=[
            DataRequired(),
            Length(min=3,max=25)
        ]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password',message='Passwords must match')
        ]
    )


