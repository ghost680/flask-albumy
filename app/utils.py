# -*- coding: utf-8 -*-

from flask import current_app, request, url_for, redirect, flash
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

from app.extensions import db
from app.config import Operations

""" 生成带时间戳的JSON web的签名 """
def generate_token(user, operation, expire_in=None, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)

    data = {'id': user.id, 'operation': operation}
    data.update(**kwargs)
    return s.dumps(data)

""" 解析并验证确认令牌 """
def validate_token(user, token, operation):
    s = Serializer(current_app.config['SECRET_KEY'])

    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False
    
    if operation != data.get('operation') or user.id != data.get('id'):
        return False
    
    if operation == Operations.CONFIRM:
        user.confirmed = True
    else:
        return False
    
    db.session.commit()
    return True