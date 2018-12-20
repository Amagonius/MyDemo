import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
#创建auth蓝图
bp = Blueprint('auth', __name__, url_prefix='/auth')

#关联了 URL /register 和 register 视图函数
@bp.route('/register', methods=('GET', 'POST'))
def register():
#验证输入
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
#验证 username 和 password 不为空
        if not username:
            error = '请输入用户名.'
        elif not password:
            error = '请输入密码.'
#验证 username 是否已被注册
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = '用户 {} 已注册'.format(username)
#插入新用户数据并提交
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = '用户名错误'
        elif not check_password_hash(user['password'], password):
            error = '密码错误'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
#检查是否登入
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
#若存在,获取用户数据	
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

#注销,清除会话
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


#检查用户登陆状态,若未登入则返回登陆页面
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view