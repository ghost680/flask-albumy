# -*- coding: utf-8 -*-

from functools import wraps
from flask import Markup, flash, url_for, redirect, abort
from flask_login import current_user

# 确认账号
def confirm_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            message = Markup(
                '请先确认您账号。'
                '没有收到激活邮件？'
                '<a class="alert-link" href="%s">重新发送确认邮件</a>' % url_for('auth.resend_confirm_email')
            )
            flash(message, 'warning')
            return redirect(url_for('main.main_index'))
        return func(*args, **kwargs)
    return decorated_function

# 权限校验
def permission_required(permission_name):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission_name):
                abort(403)
            return func(*args, **kwargs)
        return decorated_function
    return decorator

# 管理员权限
def admin_required(func):
    return permission_required('ADMINISTER')(func)

        