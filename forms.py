from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required

class Login(Form):
    nickname = TextField('nickname', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    check_me_out = BooleanField('check_me_out', default = False)