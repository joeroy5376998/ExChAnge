from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo

# Login Forms
class LoginForm(FlaskForm):
    account = StringField('帳號', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('密碼', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm(FlaskForm):
    account = StringField('帳號', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('密碼', validators=[InputRequired(), Length(min=8, max=80)])
    comfirm = PasswordField('確認密碼', validators=[InputRequired(), Length(min=8, max=80), EqualTo('password', message='密碼不一樣啦!')])

class ItemForm(FlaskForm):
    name = StringField('Item Name', validators=[InputRequired(), Length(min=1, max=15)])
    descr = StringField('Item Description', validators=[InputRequired(), Length(min=1, max=50)])

# Database
db = SQLAlchemy(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Bootstrap
bootstrap = Bootstrap(app)