import wtforms
from wtforms import validators
from models import User


class LoginForm(wtforms.Form):
	email = wtforms.StringField("Email", validators=[validators.DataRequired()])
	password = wtforms.PasswordField("Password", validators=[validators.DataRequired()])
	remember_me = wtforms.BooleanField("Remember me?", default=True)



