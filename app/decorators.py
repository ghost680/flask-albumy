# -*- coding: utf-8 -*-

from functools import wraps
from flask import Markup, flash, url_for, redirect
from flask_login import current_user

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