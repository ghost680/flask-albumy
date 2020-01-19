# -*- coding: utf-8 -*-

""" 依赖包配置 """

from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, AnonymousUserMixin
from flask_mail import Mail
from flask_dropzone import Dropzone
from flask_wtf import CSRFProtect
from flask_sitemap import Sitemap
from flask_avatars import Avatars
from flask_migrate import Migrate
from flask_moment import Moment

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
mail = Mail()
dropzone = Dropzone()
csrf = CSRFProtect()
ext = Sitemap()
avatars = Avatars()
migrate = Migrate()
moment = Moment()

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    user = User.query.get(int(user_id))
    return user

class Guest(AnonymousUserMixin):
    @property
    def is_admin(self):
        return False
    
    def can(self, permission_name):
        return False

login_manager.anonymous_user = Guest

login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'

login_manager.refresh_view = 'auth.re_authenticate'
# login_manager.needs_refresh_message = 'Your custom message'
login_manager.needs_refresh_message_category = 'warning'
