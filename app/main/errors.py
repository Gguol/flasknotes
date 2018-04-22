# -*- coding:UTF-8 -*-
from flask import render_template, jsonify
from . import main


@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='page not found')


@main.app_errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', title='internal server error')


@main.app_errorhandler(413)
def request_entity_too_large(error):
    result = dict(success=False, msg=u'文件太大，不能超过2M', file_path='')
    return jsonify(result)