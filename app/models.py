# -*- coding:UTF-8 -*-
from flask import current_app
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .crypt import MyCrypt


# 笔记模型
class Note(db.Model, UserMixin):
    __tablename__ = 'notes'

    id = db.Column(db.Integer(), primary_key=True, index=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    public = db.Column(db.Boolean())
    # 创建日期
    created_at = db.Column(db.DateTime)
    # 更新日期
    updated_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('notes', lazy='dynamic'))

    def __init__(self, title, content, public, user):
        self.title = title
        self.content = content
        self.public = public
        self.user = user

    # 生成笔记创建日期或更新日期
    def gen_time(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    # 使用AES加密文件
    def encryptContent(self):
        ec = MyCrypt(current_app.config['SECRET_KEY'])
        if not self.public:
            self.content = ec.encrypt(self.content.encode('utf-8'))

    # 解密文件
    def decryptContent(self):
        ec = MyCrypt(current_app.config['SECRET_KEY'])
        if not self.public:
            self.content = ec.decrypt(self.content)

    def printInfo(self):
        print('--'*30)
        print('title | content | public')
        print('{0} | {1} | {2}'.format(self.title, self.content[:10], self.public))
        print('--'*30)

    # 按照笔记的时间倒序列出所有的公开笔记。
    @staticmethod
    def getIndexNotes():
        notes = Note.query.filter_by(public=1).order_by(Note.created_at.desc())

        for note in notes:
            if not note.public:
                note.decryptContent()

        return notes

    # 搜索笔记功能，实现对笔记标题的模糊搜索，按照发表笔记时间从最新的开始列出。
    @staticmethod
    def getSearchNotes(keyword):
        pattern = u'%{0}%'.format(keyword)
        notes = Note.query.filter_by(public=1).filter(Note.title.ilike(pattern)).order_by(Note.created_at.desc())

        for note in notes:
            if not note.public:
                note.decryptContent()

        return notes

    # 列出已登录账号作者的所有笔记，包括公开和不公开的。
    @staticmethod
    def getUserNotes(user_id):
        notes = Note.query.filter_by(user_id=user_id).order_by(Note.created_at.desc())

        for note in notes:
            if not note.public:
                note.decryptContent()

        return notes

    # 写笔记函数，并提交
    def create(self):
        self.gen_time()
        self.encryptContent()

        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return 'error'
        return 'success'

    # 更新笔记函数，并提交
    def update(self):
        self.updated_at = datetime.now()
        self.encryptContent()

        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return 'error'
        return 'success'

    # 删除笔记函数，并提交
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return 'error'
        return 'success'

    def __repr__(self):
        return '<Note %r>' % self.title


# 创建用户模型
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, index=True)
    nick_name = db.Column(db.String(25))
    email = db.Column(db.String(40), unique=True)
    password_hash = db.Column(db.String(120))
    created_at = db.Column(db.DateTime)

    def __init__(self, email, password, nick_name):
        self.email = email
        self.password = password
        self.nick_name = nick_name

        self.gen_password()

    # 判断邮箱存在
    def exists(self, email):
        return User.query.filter_by(email=email).first() is not None

    def getDisplayName(self):
        if self.nick_name is not None:
            return self.nick_name
        else:
            return self.email.split('@')[0]

    # 用户创建，以及记录用户创建日期
    def create(self):
        if self.exists(self.email):
            return 'exists'

        self.created_at = datetime.now()

        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            return 'error'
        return 'success'

    # 生成密码散列值
    def gen_password(self):
        self.password_hash = generate_password_hash(self.password)

    # 核对用户密码散列值
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.email


