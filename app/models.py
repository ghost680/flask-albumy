# -*- coding: utf-8 -*-

from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

""" 角色权限中间表 """
roles_permissions = db.Table('roles_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)

""" 用户模型 """
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(254), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))
    website = db.Column(db.String(255))
    bio = db.Column(db.String(120))
    location = db.Column(db.String(50))
    member_since = db.Column(db.DateTime, default=datetime.now)
    confirmed = db.Column(db.Boolean, default=False) # 确认用户状态是否激活
    ip = db.Column(db.String(20))
    platform = db.Column(db.String(20)) # 操作系统
    browser = db.Column(db.String(20)) # 浏览器
    version = db.Column(db.String(20)) # 浏览器版本

    # 一个角色可以有多个用户，和用户表建立一对多关系
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', back_populates='users')

    # 和照片表建立一对多关系
    photos = db.relationship('Photo', back_populates='author', cascade='all') # 开启cascade权限，一旦用户被删除，和他相关点图片也会被删除

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 用户注册成功后自动添加角色
    def set_role(self):
        if self.role is None:
            if self.email == current_app.config['ALBUMY_ADMIN_EMAIL']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(name='User').first()

            db.session.commit()

    # 验证用户权限
    @property
    def is_admin(self):
        return self.role.name == 'Administrator'

    def can(self, permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        return permission is not None and self.role is not None and permission in self.role.permissions


""" 照片模型 """
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    filename = db.Column(db.String(64))
    filename_s = db.Column(db.String(64))
    filename_m = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.now)

    # 和用户建立一对多关系
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='photos')

""" 角色模型 """
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    # 建立和权限表的多对多关系
    permissions = db.relationship('Permission', secondary=roles_permissions, back_populates='roles')
    # 一个角色可以有多个用户，和用户表建立一对多关系
    users = db.relationship('User', back_populates='role')

    # 因为角色权限一旦确定，很少变动，在开发环境中，会频繁删除创建数据，所以把权限类型定义为角色的静态方法，方便使用
    # 静态方法，名义上是这个类的方法，但是类本身不能访问这个方法
    @staticmethod
    def init_role():
        roles_permissions_map = {
            'Locked': ['FOLLOW', 'COLLECT'], # 锁定用户
            'User': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD'], # 普通用户
            'Moderator': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'MODERATE'], # 普通管理员
            'Administrator': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'MODERATE', 'ADMINISTER'] # 超级管理员
        }

        for role_name in roles_permissions_map:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
            
            role.permissions = []
            for permission_name in roles_permissions_map[role_name]:
                permission = Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission = Permission(name = permission_name)
                    db.session.add(permission)
                
                # 多对多关系数据写入
                role.permissions.append(permission)
                
        db.session.commit()


""" 权限模型 """
class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    # 建立和角色模型的多对多关系
    roles = db.relationship('Role', secondary=roles_permissions, back_populates='permissions')

""" 淘宝店铺数据模型 """
class Taobao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_links = db.Column(db.String(120), unique=True, index=True)
    book_title = db.Column(db.String(100))
    book_price = db.Column(db.String(20))
    book_isbn = db.Column(db.String(20))
    create_time = db.Column(db.DateTime, default=datetime.now)