import secrets, os
from flask import render_template, url_for, flash, redirect, request, abort
from index.forms import Signup, Login, Posts, UpdateAccount
from index import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from index.models import User, Post


@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('afterlogin'))
    form = Signup()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, age=form.age.data,
                    city=form.city.data, phone=form.phone.data, faculty_name=str(form.Faculty_name),
                    gender=form.gender.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html', form=form, legend='Sign up')


@app.route('/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('afterlogin'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user and bcrypt.check_password_hash(user.password,form.passw.data):
            login_user(user, remember=True)

            return redirect(url_for('afterlogin'))
        else:
            flash(f'___________________________________________Wrong username or password_____________________________', 'danger')
    return render_template('login.html', form=form, legend='Log in')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/afterlogin')
def afterlogin():
    return  render_template('afterlogin.html')


@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = Posts()
    if form.validate_on_submit():
        post = Post(title=form.title.data, gender=form.gender.data,Faculty_name=str(form.Faculty_name.data), phone=form.phone.data,
                    interest=form.interest.data,description=form.app_description.data, author=current_user)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('posting.html', form=form, legend='Add Post')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route('/account',  methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.age = form.age.data
        current_user.city = form.city.data
        current_user.phone = form.phone.data
        current_user.gender = form.gender.data
        current_user.faculty_name = form.Faculty_name.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.age.data = current_user.age
        form.city.data = current_user.city
        form.phone.data = current_user.phone
        form.gender.data = current_user.gender
        form.Faculty_name.data = current_user.faculty_name

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form, legend='Update your info:')


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = Posts()
    if form.validate_on_submit():
        post.title = form.title.data
        post.gender = form.gender.data
        post.Faculty_name = form.Faculty_name.data
        post.phone = form.phone.data
        post.interest = form.interest.data
        post.description = form.app_description.data
        db.session.commit()
        flash('your post has been updated', 'success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.name.data = current_user.username
        form.gender.data = post.gender
        form.Faculty_name.data = post.Faculty_name
        form.phone.data = post.phone
        form.interest.data = post.interest
        form.app_description.data = post.description
    return render_template('posting.html', form=form, legend='Update Post')
