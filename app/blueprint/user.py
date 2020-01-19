# -*- coding: utf-8 -*-

from flask import render_template, Blueprint, request, current_app
from flask_login import login_required
from app.models import User, Photo

user_bp = Blueprint('user', __name__)

""" 个人中心 """
@user_bp.route('/<username>')
@login_required
def index(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_PHOTO_PER_PAGE']
    pagination = Photo.query.with_parent(user).order_by(Photo.timestamp.desc()).paginate(page, per_page)
    photos = pagination.items

    return render_template('user/index.html', user=user, pagination=pagination, photos=photos)

@user_bp.route('/afda')
@login_required
def unfollow():
    return render_template('user/index.html')

@user_bp.route('/dasf')
@login_required
def follow():
    return render_template('user/index.html')



