# -*- coding:UTF-8 -*-
from wtforms import Form
from wtforms import BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email


# 注册表单
class SignupForm(Form):
    email = StringField('邮箱', validators=[
        Email(), DataRequired(), Length(min=5, max=40)
    ])
    nick_name = StringField('昵称', validators=[
        Length(min=3, max=25)
    ])
    password = PasswordField('密码', validators=[
        DataRequired(), Length(min=6, max=30), EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('确认密码')


# 登录表单
class LoginForm(Form):
    email = StringField('邮箱', validators=[
        DataRequired(), Email(), Length(min=5, max=40)
    ])
    password = PasswordField('密码', validators=[
        DataRequired(), Length(min=6, max=30)
    ])
    remember = BooleanField('记住我')