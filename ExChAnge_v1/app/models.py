from flask_login import UserMixin
from .extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_account = db.Column(db.String(15), unique=True)
    user_password = db.Column(db.String(80))

class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(15))
    item_pic_path = db.Column(db.LargeBinary)
    item_status = db.Column(db.Integer())
    item_owner_id = db.Column(db.Integer())
    item_post_id = db.Column(db.Integer())