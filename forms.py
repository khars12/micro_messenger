from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required

class LoginForm(FlaskForm):
    nickname = TextField('nickname', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    check_me_out = BooleanField('check_me_out', default = False)

class ConfirmForm(FlaskForm):
    confirm_password = PasswordField('password', validators = [Required()])

class NewChatForm(FlaskForm):
    query = TextField('query')

class SettingsForm(FlaskForm):
    new_nickname = TextField('new_nickname')
    new_password = PasswordField('new_password')
    confirm_new_password = PasswordField('confirm_new_password')

class MessageForm(FlaskForm):
    message = TextField('message', validators = [Required()])