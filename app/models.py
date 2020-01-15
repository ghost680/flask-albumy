# -*- coding: utf-8 -*-

from datetime import datetime
from flask_login import UserMixin
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


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
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False) # 确认用户状态是否激活
    ip = db.Column(db.String(20))
    platform = db.Column(db.String(20)) # 操作系统
    browser = db.Column(db.String(20)) # 浏览器
    version = db.Column(db.String(20)) # 浏览器版本

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

""" 淘宝店铺数据模型 """
class Taobao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_links = db.Column(db.String(120), unique=True, index=True)
    book_title = db.Column(db.String(100))
    book_price = db.Column(db.String(20))
    book_isbn = db.Column(db.String(20))
    create_time = db.Column(db.DateTime, default=datetime.now)