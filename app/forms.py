from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import Required



class LoginForm(FlaskForm):
    nickname = StringField(validators=[Required()])
    password = PasswordField(validators=[Required()])
    rememberme = BooleanField("Remember me", default=False)
    # Submit button is in html file


class SignupForm(FlaskForm):
    confirm_password = PasswordField(validators=[Required()])
    confirm_password_submit = SubmitField("Sign up")


class ConfirmForm(FlaskForm):
    confirm_password = PasswordField(validators=[Required()])
    confirm_password_submit = SubmitField("Confirm")


class NewChatForm(FlaskForm):
    query = StringField()
    # Submit button is in html file


class SettingsForm(FlaskForm):
    new_nickname = StringField()
    new_password = PasswordField()
    confirm_new_password = PasswordField()
    change_settings_submit = SubmitField("Change settings")


class MessageForm(FlaskForm):
    message = StringField(validators=[Required()])
    message_submit = SubmitField("Send")