# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

from app.models import User

""" 登录表单 """
class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 254), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

""" 注册表单 """
class RegisterForm(FlaskForm):
    name = StringField('昵称', validators=[DataRequired(), Length(1, 30)])
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 254), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20), Regexp('^[a-zA-Z0-9]*$', message='用户名应该由字母数字组成')])
    password = PasswordField('密码', validators=[DataRequired(), Length(8, 128), EqualTo('rePassword')])
    rePassword = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('这个邮箱已经注册了，请直接登录')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('这个用户名已经被使用')

""" 找回密码 """
class ForgetPasswordForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField('找回密码')

""" 重置密码 """
class ResetPasswordForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 254), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(8, 128), EqualTo('rePassword')])
    rePassword = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('重置密码')