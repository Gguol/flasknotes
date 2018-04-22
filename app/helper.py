# -*- coding:UTF-8 -*-
import glob
import os
from flask_login import current_user


# 返回笔记的URL，不公开则返回id公开返回当前用户昵称和笔记id
def getNoteUrl(note):
    if note.public:
        return '/note/{0}'.format(note.id)
    else:
        return '/{0}/{1}'.format(current_user.nick_name, note.id)


# glob.glob返回所有匹配的文件路径列表
def emptyDir(dir):
    files = glob.glob(os.path.join(dir, '*'))
    for f in files:
        print(f)
        os.remove(f)


class Helper:
    @staticmethod
    def init_app(app):
        @app.context_processor
        def utility_processor():
            return dict(getNoteUrl=getNoteUrl)
