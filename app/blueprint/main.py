# -*- coding: utf-8 -*-

import os

from flask import Blueprint, render_template, request, current_app, send_from_directory, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from flask_dropzone import random_filename

from app.decorators import confirm_required, permission_required
from app.extensions import db
from app.forms.main import DescriptionForm, TagForm, CommentForm
from app.models import Photo
from app.utils import resize_image

main_bp = Blueprint('main', __name__)

""" 网站入口 """
@main_bp.route('/', methods=['GET'])
def main_index():
    return render_template('main/index.html')

""" 获取头像 """
@main_bp.route('/avatars/<path:filename>')
@login_required
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)

""" 获取图片 """
@main_bp.route('/upload/<path:filename>')
@login_required
@confirm_required # 验证确认状态
def get_image(filename):
    return send_from_directory(current_app.config['ALBUMY_UPLOAD_PATH'], filename)

""" 图片上传 """
@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required # 验证登录状态
@confirm_required # 验证确认状态
@permission_required('UPLOAD') # 验证权限
def upload():
    if request.method == 'POST' and 'file' in request.files:
        f = request.files.get('file') # 获取图片对象
        filename = random_filename(f.filename) # 重命名文件
        f.save(os.path.join(current_app.config['ALBUMY_UPLOAD_PATH'], filename)) # 保存图片文件到服务器目录
        filename_s = resize_image(f, filename, current_app.config['ALBUMY_PHOTO_SIZE']['small'])
        filename_m = resize_image(f, filename, current_app.config['ALBUMY_PHOTO_SIZE']['medium'])

        # 创建图片的数据库记录
        photo = Photo(
            filename = filename,
            filename_s = filename_s,
            filename_m = filename_m,
            # 这里使用author关系属性与用户建立关系，需要对代理对象current_user调用_get_current_object方法获取真实用户对象，而不是使用代理对象current_user
            author = current_user._get_current_object()
        )

        db.session.add(photo)
        db.session.commit()
    return render_template('main/upload.html')

""" 浏览 """ 
@main_bp.route('/explore', methods=['GET'])
@login_required
@confirm_required # 验证确认状态
def explore():
    return render_template('main/explore.html')

""" 查看图片 """
@main_bp.route('/photo/<int:photo_id>', methods=['GET'])
@login_required
@confirm_required # 验证确认状态
def show_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_COMMENT_PER_PAGE']
    # pagination = Comment.query.with_parent(photo).order_by(Comment.timestamp.asc()).paginate(page, per_page)
    # comments = pagination.items

    comment_form = CommentForm()
    description_form = DescriptionForm()
    tag_form = TagForm()

    description_form.description.data = photo.description
    return render_template('main/photo.html', 
        photo=photo, 
        comment_form=comment_form,
        tag_form=tag_form,
        description_form=description_form,
        # pagination=pagination
    )

""" 查看下一张图片 """
@main_bp.route('/photo/n/<int:photo_id>')
@login_required
@confirm_required # 验证确认状态
def photo_next(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    photo_n = Photo.query.with_parent(photo.author).filter(Photo.id < photo_id).order_by(Photo.id.desc()).first()

    if photo_n is None:
        flash('这已经是最后一张图片了', 'info')
        return redirect(url_for('.show_photo', photo_id=photo_id))
    return redirect(url_for('.show_photo', photo_id=photo_n.id))

""" 查看上一张 """
@main_bp.route('/photo/p/<int:photo_id>')
@login_required
@confirm_required # 验证确认状态
def photo_previous(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    photo_p = Photo.query.with_parent(photo.author).filter(Photo.id > photo_id).order_by(Photo.id.asc()).first()

    if photo_p is None:
        flash('这已经是最后一张图片了', 'info')
        return redirect(url_for('.show_photo', photo_id=photo_id))
    return redirect(url_for('.show_photo', photo_id=photo_p.id))

""" 删除图片 """
@main_bp.route('/delete/photo/<int:photo_id>', methods=['POST'])
@login_required
@confirm_required # 验证确认状态
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author and not current_user.can('MODERATE'):
        abort(403)
    
    db.session.delete(photo)
    db.session.commit()
    flash('照片删除成功', 'info')
    
    photo_n = Photo.query.with_parent(photo.author).filter(Photo.id < photo_id).order_by(Photo.id.desc()).first()
    if photo_n is None:
        photo_p = Photo.query.with_parent(photo.author).filter(Photo.id > photo_id).order_by(Photo.id.asc()).first()
        if photo_p is None:
            return redirect(url_for('user.index', username=photo.author.username))
        return redirect(url_for('.show_photo', photo_id=photo_p.id))
    return redirect(url_for('.show_photo', photo_id=photo_n.id))

""" 举报图片 """
@main_bp.route('/report/photo/<int:photo_id>', methods=['POST'])
@login_required
@confirm_required # 验证确认状态
def report_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    photo.flag += 1
    db.session.commit()
    flash('举报成功', 'success')
    return redirect(url_for('.show_photo', photo_id=photo.id))

