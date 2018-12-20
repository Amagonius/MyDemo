from flask import render_template, redirect, url_for, g, session, flash
from sqlalchemy.sql.functions import current_user
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash

from app import app, db
from app.forms import LoginForm, RegisterForm, PostForm, CreateForm, UpdateForm
from app.models import User, Post


@app.route('/')
@app.route('/index')
@login_required
def index():
    # form = PostForm()
    # if form.validate_on_submit():
    #     post = Post(body=form.post.data, author_id=current_user)
    #     db.session.add(post)
    #     db.session.commit()
    #     return redirect(url_for('index'))
    username = current_user.username
    posts = Post.query.order_by(Post.id).all()
    return render_template('index.html', title='主页', username=username, posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # 注册
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        # user.password = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功!')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 登录
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        #if user is None or not user.check_password(form.password.data):
        if user is None or user.password != form.password.data:
            flash('用户名或密码错误!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='登陆', form=form)


@app.route('/logout')
def logout():
    # 注销
    logout_user()
    return redirect(url_for('index'))


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # 新建
    if current_user.is_authenticated:
        form = CreateForm()
        if form.validate_on_submit():
            post = Post(title=form.title.data, body=form.body.data)
            db.session.add(post)
            db.session.commit()
            flash('创建成功!')
            return redirect(url_for('index'))
    return render_template('create.html', title='新建', form=form)


@app.route('/<id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    form = UpdateForm()
    post = Post.query.filter_by(id=id).first()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        return redirect('index')
    return render_template('update.html',title='编辑', form=form)