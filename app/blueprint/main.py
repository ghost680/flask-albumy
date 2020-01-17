# -*- coding: utf-8 -*-

import os

from flask import Blueprint, render_template, request, current_app
from flask_login import login_required, current_user
from flask_dropzone import random_filename

from app.decorators import confirm_required, permission_required
from app.extensions import db
from app.models import Photo
from app.utils import resize_image

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def main_index():
    return render_template('main/index.html')

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