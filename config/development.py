# -*- coding:UTF-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


def getDatabasePath(name):
    return 'sqlite:///' + os.path.join(basedir, os.path.pardir, 'db', name)


def getTmpDir(dirname):
    return os.path.join(basedir, os.path.pardir, dirname)


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or getDatabasePath('snote-dev.db')
    # 不要让其他人知道
    SECRET_KEY = '1234567890abcdef'
    MAX_CONTENT_LENGTH = os.environ.get('MAX_CONTENT_LENGTH') or 2 * 1024 * 1024
    # 每次请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 每页笔记卡片的数量
    NOTE_NUM_PER_PAGE = 12

    TMP_DIR = getTmpDir('.tmp')
    # 七牛云
    QINIU_DOMAIN = 'http://p6nf5qfql.bkt.clouddn.com/'
    QN_ACCESS_KEY = '3znUn24LJWDTrOCR-Fh7TtHOI3xKREarLPCrhP37'
    QN_SECRET_KEY = '6xCC-fOzgaRioEakyDPw02vq-8EICtJEGP8TnZjo'
    QN_BUCKET_NAME = 'guolei-qiniustorage'

    @staticmethod
    def init_app(app):
        app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
