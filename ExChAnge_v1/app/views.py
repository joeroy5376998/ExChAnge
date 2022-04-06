import os
import uuid
from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .extensions import login_manager, bootstrap, db, LoginForm, RegisterForm, ItemForm
from .models import User, Item, Post

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/homepage')
def index():
    items_list = []
    post_items = Post.query.all()
    for post_item in post_items :
        item = Item.query.filter_by(item_id=post_item.post_item_id).first()
        items_list.append(item)

    return render_template('homepage.html', post_items=items_list)

@app.route('/about')
def about():
    return render_template('aboutUs.html')

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_account=form.account.data).first()
        if user:
            if check_password_hash(user.user_password, form.password.data):
                logout_user()
                login_user(user)
                return redirect(url_for('bag'))
            
        flash("帳密錯誤!", "info")
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        duplicate_name = User.query.filter_by(user_account=form.account.data).count()
        if not duplicate_name:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(user_account=form.account.data, user_password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("註冊成功！請登入!", "info")
            return redirect(url_for("login"))
        else:
            flash("帳號已被使用！", "info")
            return redirect(url_for("signup"))

    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/bag')
@login_required
def bag():
    items = Item.query.filter_by(item_owner_id=current_user.id)
    return render_template('backpack.html', bag=items)

@app.route('/upload_item', methods=['GET', 'POST'])
@login_required
def upload_item():
    form = ItemForm()
    if form.validate_on_submit():
        image = form.image.data
        filename = secure_filename(image.filename)
        rand = uuid.uuid4()
        path = os.path.join(app.root_path,'static', 'uploads', f"{str(rand)}_{filename}")
        image.save(path)
        new_item = Item(item_name=form.name.data, item_owner_id=current_user.id, \
                        item_pic_filename= f"{str(rand)}_{filename}", item_status=0)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("bag"))

    return render_template('uploadpage.html', form=form)

@app.route('/delete_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    item = Item.query.filter_by(item_id=item_id).first()
    if item != None and current_user.id == item.item_owner_id:
        # Remove entry from bag table, remove photo from os directory
        path = os.path.join(app.root_path,'static', 'uploads', item.item_pic_filename)
        os.remove(path)
        db.session.delete(item)
        # Remove entry from post table
        post = Post.query.filter_by(post_item_id=item_id).first()
        if post != None:
            db.session.delete(post)
        
        # Remember to remove candidate of this item from the candidate table
        db.session.commit()

    return redirect(url_for('bag'))

@app.route('/post_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def post_item(item_id):
    item = Item.query.filter_by(item_id=item_id).first()
    if item.item_status == 0 and current_user.id == item.item_owner_id:
        # Change status of item to 1: posted
        item.item_status = 1
        # Add new entry into post table
        new_post = Post(post_item_id=item_id)
        db.session.add(new_post)
        db.session.commit()

    return redirect(url_for("bag"))

@app.route('/unpost_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def unpost_item(item_id):
    item = Item.query.filter_by(item_id=item_id).first()
    if item.item_status == 1 and current_user.id == item.item_owner_id :
        # Change status of item to 0: no_status
        item.item_status = 0
        # Remove entry from post table
        post = Post.query.filter_by(post_item_id=item_id).first()
        if post != None:
            db.session.delete(post)
            
        # Remember to remove candidate of this item from the candidate table
        db.session.commit()

    return redirect(url_for("bag"))