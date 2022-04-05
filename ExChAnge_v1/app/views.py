from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import login_manager, bootstrap, db, LoginForm, RegisterForm, ItemForm
from .models import User, Item

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/bag')
def bag():
    return render_template('bag.html')
    
"""
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = ItemForm()
    if form.validate_on_submit():
        new_item = Item(item_name=form.name.data, item_descr=form.descr.data, item_owner_id=current_user.id)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template('upload.html', form=form)
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(user_account=form.account.data).first()
        if user:
            if check_password_hash(user.user_password, form.password.data):
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
            flash("註冊成功！", "info")
            return redirect(url_for("login"))
        else:
            flash("帳號已被使用！", "info")
            return redirect(url_for("signup"))

    return render_template('signup.html', form=form, test=form.account.data, test2=form.password.data, test3=form.comfirm.data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


