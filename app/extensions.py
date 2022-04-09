from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo

# Login Forms
class LoginForm(FlaskForm):
    account = StringField('帳號', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('密碼', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm(FlaskForm):
    account = StringField('帳號', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('密碼', validators=[InputRequired(), Length(min=8, max=80)])
    confirm = PasswordField('確認密碼', validators=[InputRequired(), Length(min=8, max=80), EqualTo('password', message='密碼不一樣啦!')])

class ItemForm(FlaskForm):
    name = StringField('', validators=[InputRequired(), Length(min=1, max=15)])
    image = FileField('', validators=[FileRequired(), FileAllowed(['jpg', 'png'], '只能傳圖片啦!')])

# Database
db = SQLAlchemy(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = '請先登入才能造訪此頁!'
login_manager.login_view = 'login'

# Bootstrap
bootstrap = Bootstrap(app)