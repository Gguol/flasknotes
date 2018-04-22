# -*- coding=UTF-8 -*-
from flask import url_for, redirect
from . import main


# 主页
@main.route('/')
def index():
    return redirect(url_for('note.show_public_notes'))
