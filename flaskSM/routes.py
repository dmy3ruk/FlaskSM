import os
import secrets

from flask import Flask, render_template, request, flash, redirect, url_for
from flask import  render_template, request
from werkzeug.utils import secure_filename

from flaskSM.forms import LoginForm, RegistrationForm, PostForm, EditProfileForm, EditPostForm
from flaskSM.models import User, Post
from flaskSM import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/', methods=['GET', 'POST'])
def signUp():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.add(User(username=form.username.data, email=form.email.data, password=hashed_password))
        db.session.commit()
        print("Form validated successfully.")
        return redirect('dashboard')
    return render_template('signUp.html', form=form, title='Registration')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print("Logged in successfully.")
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('hello_world'))
        else:
            flash("Unsuccessful login. Please check email and password")
            print('Invalid')
    else:
        print('Invalid form')
    return render_template('signIn.html', form=form, title='Login')

def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def hello_world():
    posts = Post.query.limit(30).all()
    return render_template('index.html', posts=posts)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm()
    edit_post_form = EditPostForm()
    posts = Post.query.filter_by(user_id=current_user.id).all()
    count=0
    print(posts)
    for i in posts:
        count+=1
    print(count)
    profile_img=url_for('static', filename='profile_pic/' + current_user.image_file)

    if form.validate_on_submit():
        update_profile(form)

    post_id = request.form.get('post_id')
    if edit_post_form.validate_on_submit():
        update_post(edit_post_form, post_id)

    return render_template('profile.html', profile_img=profile_img,
                           posts=posts, count=count, form=form, edit_post_form=edit_post_form)

def update_profile(form):
    user = User.query.filter_by(username=current_user.username).first()
    if form.file.data:
        picture = save_picture(form.file.data)
        current_user.image_file = picture
        db.session.commit()  # Зберігаємо зміни в базі даних
        flash('Profile updated successfully!', 'success')
    else:
        picture = None
    user.bio = form.bio.data
    user.username = form.username.data
    user.email = form.email.data
    db.session.commit()

def update_post(form, post_id):
    post = Post.query.get(post_id)
    if post and post.user_id == current_user.id:
        form.title.data = post.title
        form.content.data = post.content
        db.session.commit()
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/post_img', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        title=form.title.data
        content=form.content.data
        if form.file.data:
            picture=save_picture(form.file.data)
        else:
            picture = None
        post = Post(title=title, content=content, file=picture, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        print("post added")
    return render_template('create.html', form=form, title='Post')


@app.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    return render_template('explore.html')


@app.route('/activity', methods=['GET', 'POST'])
@login_required
def activity():
    return render_template('activity.html')


@app.route('/inbox', methods=['GET', 'POST'])
@login_required
def inbox():
    return render_template('inbox.html')

