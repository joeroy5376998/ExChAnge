import os
import uuid
from app import app
from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .extensions import login_manager, bootstrap, db, LoginForm, RegisterForm, ItemForm
from .models import User, Item, Post, Candidate

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    items_list = []
    post_items = Post.query.all()
    for post_item in reversed(post_items) :
        item = Item.query.filter_by(item_id=post_item.post_item_id).first()
        items_list.append(item)

    return render_template('homepage.html', post_items=items_list)

@app.route('/about')
def about():
    return render_template('aboutUs.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_account=form.account.data).first()
        if user:
            if check_password_hash(user.user_password, form.password.data):
                logout_user()
                login_user(user)
                session['user_account'] = current_user.user_account
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
                        item_pic_filename=f"{str(rand)}_{filename}", item_status=0)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('bag'))

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
        # Assign post id to item
        post = Post.query.filter_by(post_item_id=item_id).first()
        item.item_post_id = post.post_id

        db.session.commit()

    return redirect(url_for("bag"))

@app.route('/get_post_id/<int:post_id>/<string:page>', methods=['GET', 'POST'])
@login_required
def get_post_id(post_id, page):
    if page == 'sel_bag':
        return redirect(url_for("select_bag_item", post_id=post_id))
    else :
        return redirect(url_for("select_candidate", post_id=post_id))

@app.route('/select_bag_item', methods=['GET', 'POST'])
@login_required
def select_bag_item():
    items = Item.query.filter_by(item_owner_id=current_user.id, item_status=0)
    return render_template('select_from_bag.html', bag=items, post_id=request.args['post_id'])

@app.route('/add_candidate/<int:item_id>/<int:post_id>', methods=['GET', 'POST'])
@login_required
def add_candidate(item_id, post_id):
    item = Item.query.filter_by(item_id=item_id).first()
    if item.item_status == 0 and item.item_owner_id == current_user.id:
        new_candidate = Candidate(post_id=post_id, item_id=item_id)
        # Change status of item to 2: candidated
        item.item_status = 2
        db.session.add(new_candidate)
        db.session.commit()

    return redirect(url_for("index"))

@app.route('/select_candidate', methods=['GET', 'POST'])
@login_required
def select_candidate():
    candidate_items_id = [candidate.item_id for candidate in Candidate.query.filter_by(post_id=request.args['post_id'])]
    items = []
    for id in candidate_items_id:
        items.append(Item.query.filter_by(item_id=id).first())

    return render_template('select_candidate.html', bag=items, post_id=request.args['post_id'])

@app.route('/exchange/<int:item_id>/<int:post_id>', methods=['GET', 'POST'])
@login_required
def exchange(item_id, post_id):
    item = Item.query.filter_by(item_post_id=post_id).first()
    if item.item_owner_id == current_user.id:
        # Set its candidate's status back to 0: no_status or 3: completed
        candidate_items_id = [candidate.item_id for candidate in Candidate.query.filter_by(post_id=item.item_post_id)]
        for id in candidate_items_id :
            candidate_item = Item.query.filter_by(item_id=id).first()
            if candidate_item.item_id == item_id :
                candidate_item.item_status = 3
            else:
                candidate_item.item_status = 0

            # Remove candidates of this item from the candidate table
            Candidate.query.filter_by(post_id=item.item_post_id).delete()
            # Remove post entry from post table
            Post.query.filter_by(post_item_id=item.item_id).delete()
            # Change status of item to 0: no_status
            item.item_status = 3
            # Remove post id from item
            item.item_post_id = None

            flash("success")
            db.session.commit()

    return redirect(url_for('bag'))

"""
@app.route('/unpost_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def unpost_item(item_id):
    item = Item.query.filter_by(item_id=item_id).first()
    if item.item_status == 1 and current_user.id == item.item_owner_id :
        # Set its candidate's status back to 0: no_status
        candidate_items_id = [candidate.item_id for candidate in Candidate.query.filter_by(post_id=item.item_post_id)]
        for id in candidate_items_id :
            candidate_item = Item.query.filter_by(item_id=id).first()
            candidate_item.item_status = 0

        # Remove candidates of this item from the candidate table
        Candidate.query.filter_by(post_id=item.item_post_id).delete()
        # Remove post entry from post table
        Post.query.filter_by(post_item_id=item_id).delete()
        # Change status of item to 0: no_status
        item.item_status = 0
        # Remove post id from item
        item.item_post_id = None

        db.session.commit()

    return redirect(url_for("bag"))
"""