# -*- coding:UTF-8 -*-
from flask import Blueprint

note = Blueprint('note', __name__)

from . import views