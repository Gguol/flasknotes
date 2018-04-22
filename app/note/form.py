# -*- coding:UTF-8 -*-
from wtforms import Form
from wtforms import BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


# 创建笔记文章表单
class CreateNoteForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    # render_kw字典 把一些属性以键值对的形式添加到字段中
    content = TextAreaField(' ', validators=[DataRequired()], render_kw={"id": "editor"})
    public = BooleanField('Public', render_kw={"title": "Others can view."})


# 编辑文章表单
class EditNoteForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    content = TextAreaField(' ', validators=[DataRequired()], render_kw={"id": "editor"})
    public = BooleanField('Public', render_kw={"title": "Others can view."})