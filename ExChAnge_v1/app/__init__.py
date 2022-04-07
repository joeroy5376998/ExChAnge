from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/database.db'
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
from app import views
