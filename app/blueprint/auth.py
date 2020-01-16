# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login
from app.forms.auth import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from app.models import User
from app.extensions import db, login_manager
from app.utils import generate_token, validate_token, redirect_back
from app.config import Operations
from app.emails import send_confirm_email, send_reset_password_email

auth_bp = Blueprint('auth', __name__)


""" 登录 """
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.main_index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.validate_password(form.password.data):
            if login_user(user, form.remember_me.data):
                flash('登录成功', 'info')
                return redirect_back()
            else:
                flash('您的账号已被锁定，请联系管理员', 'warning')
                return redirect(url_for('main.main_index'))
        flash('无效的邮箱或密码', 'warning')
    return render_template('auth/login.html', form=form)


""" 注册 """
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.main_index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        ip = request.remote_addr
        platform = request.user_agent.platform
        browser = request.user_agent.browser
        version = request.user_agent.version
        
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
        flash('激活邮件已发送到您的邮箱，请查收', 'success')
        return redirect(url_for('.login'))

    return render_template('auth/reg.html', form=form)


""" 找回密码 """
@auth_bp.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.main_index'))

    form = ForgetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = generate_token(user=user, operation=Operations.RESET_PASSWORD)
            send_reset_password_email(user=user, token=token)
            flash('密码重置邮件已发送，请检查您的邮箱', 'info')
            return redirect(url_for('.login'))
        
        flash('无效的邮箱', 'warning')
        return redirect(url_for('.forget_password'))
    return render_template('auth/reset_password.html', form=form)

""" 重置密码 """
@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.main_index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        
        if user is None:
            return redirect(url_for('main.main_index'))
        
        if validate_token(user=user, token=token, operation=Operations.RESET_PASSWORD, new_password=form.password.data):
            flash('密码更新成功', 'success')
            return redirect(url_for('.login'))
        else:
            flash('链接无效或已过期', 'danger')
            return redirect(url_for('.forget_password'))
    return render_template('auth/reset_password.html', form=form)

""" 确认账号 """
@auth_bp.route('/confirm/<token>', methods=['GET'])
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.main_index'))
    
    if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
        flash('账号激活成功', 'success')
        return redirect(url_for('main.main_index'))
    else:
        flash('无效或令牌已过期', 'danger')
        return redirect(url_for('.resend_confirm_email'))


""" 重新发送激活邮件 """
@auth_bp.route('/resend_confirm_email', methods=['GET'])
@login_required
def resend_confirm_email():
    if current_user.confirmed:
        return redirect(url_for('main.main_index'))
    
    token = generate_token(user=current_user, operation=Operations.CONFIRM)
    send_confirm_email(user=current_user, token=token)
    flash('新的激活邮件已发送，请检查你的邮箱', 'info')
    return redirect(url_for('main.main_index'))
