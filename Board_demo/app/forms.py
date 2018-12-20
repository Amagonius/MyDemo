from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length

from app.models import User, Post


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=2, max=16, message="用户名长度为2-16字符")])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登陆')


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=2, max=8, message="密码长度为2-8字符")])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名已存在!')


class PostForm(FlaskForm):
    post = StringField('post', validators=[DataRequired()])
    submit = SubmitField('提交')


class CreateForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    body = TextAreaField("内容", validators=[DataRequired(message="内容不能为空")])
    submit = SubmitField('新建')

    def validate_title(self, title):
        post = Post.query.filter_by(title=title.data).first()
        if post is not None:
            raise ValidationError('该条目已存在!')


class UpdateForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    body = TextAreaField("内容", validators=[DataRequired(message="内容不能为空")])
    submit = SubmitField('编辑')