from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, HiddenField
from wtforms.validators import EqualTo, InputRequired, Length, Regexp, ValidationError

from app.messenger_functions import delete_user



class JustNickForm(FlaskForm):
    nickname = StringField(render_kw={'autofocus': True}, validators=[
        Length(min=4, message="Minimum nickname length is 4."), 
        Length(max=20, message="Maximum nickname length is 20."), 
        Regexp(r'[A-Za-z0-9_]*$', message="Nickname can only use letters, numbers and underscores.")
    ])


class SignInForm(FlaskForm):
    password = PasswordField(render_kw={'autofocus': True}, validators=[
        Length(min=5, message="Minimum password length is 5."), 
        Length(max=20, message="Maximum password length is 20."), 
        Regexp(r'[!-}]*$', message="Password can only use letters, numbers and some other symbols.")
    ])
    rememberme = BooleanField("Remember me", default=False)
    signin_submit = SubmitField("Sign in")


class SignUpForm(FlaskForm):
    password = PasswordField(render_kw={'autofocus': True}, validators=[
        Length(min=5, message="Minimum password length is 5."), 
        Length(max=20, message="Maximum password length is 20."), 
        Regexp(r'[!-}]*$', message="Password can only use letters, numbers and some other symbols.")
    ])
    confirm_password = PasswordField(validators=[EqualTo('password', message='Entered passwords must be equal.')])
    signup_submit = SubmitField("Sign up")


class ConfirmForm(FlaskForm):
    confirm_password = PasswordField(render_kw={'autofocus': True}, validators=[InputRequired()])
    confirm_password_submit = SubmitField("Confirm")


class NewChatForm(FlaskForm):
    query = StringField(render_kw={'autofocus': True})


def check_new_nickname_min_length(form, field):
    if len(field.data) > 0:
        if len(field.data) < 4:
            raise ValidationError("Minimum nickname length is 4.")


def check_new_password_min_length(form, field):
    if len(field.data) > 0 and len(field.data) < 4:
        raise ValidationError("Minimum password length is 4.")


def new_nickname_or_password_or_delete_user(form, field):
    if not (form.new_nickname.data or form.new_password.data or form.delete_user.data):
        raise ValidationError("")


class SettingsForm(FlaskForm):
    current_password = PasswordField(render_kw={'autofocus': True}, validators=[
        Length(min=1, message="Enter current password.")
    ])

    new_nickname = StringField(validators=[
        new_nickname_or_password_or_delete_user,
        check_new_nickname_min_length,
        Length(max=20, message="Maximum nickname length is 20."), 
        Regexp(r'[A-Za-z0-9_]*$', message="Nickname can only use letters, numbers and underscores."),
    ])

    new_password = PasswordField(validators=[
        new_nickname_or_password_or_delete_user,
        check_new_password_min_length, 
        Length(max=20, message="Maximum password length is 20."), 
        Regexp(r'[!-}]*$', message="Password can only use letters, numbers and some other symbols.")
    ])

    confirm_new_password = PasswordField(validators=[EqualTo("new_password", message="Passwords aren't equal.")])

    delete_user = HiddenField(render_kw={'value': False})

    change_settings_submit = SubmitField("Change settings")


class MessageForm(FlaskForm):
    message = StringField(render_kw={'autofocus': True}, )
    message_submit = SubmitField("Send")