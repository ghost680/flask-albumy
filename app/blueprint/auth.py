# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login
from app.forms.auth import RegisterForm
from app.models import User
from app.extensions import db, login_manager
from app.utils import generate_token
from app.config import Operations
from app.emails import send_confirm_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.main_index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data.lower()
        username = form.username.data
        ip = request.remote_addr
        platform = request.user_agent.platform
        browser = request.user_agent.browser
        version = request.user_agent.version
        password = form.username.data
        
        # 数据入库
        user = User(
            name=name, 
            email=email,
            username=username,
            ip = ip,
            platform = platform,
            browser = browser,
            version = version
        )

        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        token = generate_token(user=user, operation=Operations.CONFIRM)
        send_confirm_email(user=user, token=token)
        flash('激活邮件已发送到您的邮箱，请查收')
        return redirect(url_for('.login'))

    return render_template('auth/reg.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')

""" 确认账号 """
@auth_bp.route('/confirm', methods=['GET', 'POST'])
def confirm():
    return render_template('auth/confirm.html')
