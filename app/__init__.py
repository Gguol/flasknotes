# -*- coding:UTF-8 -*-
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config
from .helper import Helper
from .upload import Upload

login_manager = LoginManager()
# 设置强安全等级防止回话遭篡改
login_manager.session_protection = 'strong'
# 设置登录页面的端点
login_manager.login_view = 'user.login'
db = SQLAlchemy()


# 使用程序工厂函数，可用于在不同配置环境中运行
def create_app(config_name):
    # static_url_path主要用于改变url的path的，静态文件放在static下面，
    # 所以正常情况url是static/filename ，但是可以通过static_url_path来改变这个url
    app = Flask(__name__, static_url_path='')

    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    Helper.init_app(app)

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

    # 注册蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from .note import note as note_blueprint
    app.register_blueprint(note_blueprint)

    return app

