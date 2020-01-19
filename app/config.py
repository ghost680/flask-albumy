# -*- coding: utf-8 -*-

import os
import sys
import mysql.connector

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
platform = sys.platform

if platform == 'win32':
  db_url = 'mysql+mysqlconnector://root@localhost:3306/albumy_db'
elif platform == 'darwin':
  db_url = 'mysql+mysqlconnector://root:123456@localhost:3306/albumy_db'
else:
  db_url = 'mysql+mysqlconnector://ghost2020:GHOST2018@kpw%@localhost:20120/albumy_db'

class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'
    
class BaseConfig(object):
  SECRET_KEY = os.getenv('SECRET_KEY', '0487f30a81244b6ea8c6de8ca81feba6')

  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_RECORD_QUERIES = True
  SQLALCHEMY_POOL_RECYCLE = 280

  SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS = True
  SITEMAP_BLUEPRINT_URL_PREFIX = '/'

  DROPZONE_MAX_FILE_SIZE = 2
  DROPZONE_MAX_FILES = 20
  DROPZONE_ALLOWED_FILE_TYPE = 'image'
  DROPZONE_ENABLE_CSRF = True
  MAX_CONTENT_LENGTH = 2 * 1024 * 1024

  APP_PER_PAGE = 20
  ALBUMY_PHOTO_PER_PAGE = 16
  ALBUMY_COMMENT_PER_PAGE = 10

  ALBUMY_MAIL_SUBJECT_PREFIX = '[Albumy]'
  ALBUMY_ADMIN_EMAIL = os.getenv('ALBUMY_ADMIN', 'ghost2019@qq.com')
  ALBUMY_UPLOAD_PATH = os.path.join(basedir, 'uploads')
  ALBUMY_PHOTO_SIZE = {'small': 400, 'medium': 800}
  ALBUMY_PHOTO_SUFFIX = {
    ALBUMY_PHOTO_SIZE['small']: '_s',  # thumbnail
    ALBUMY_PHOTO_SIZE['medium']: '_m',  # display
  }

  AVATARS_SAVE_PATH = os.path.join(ALBUMY_UPLOAD_PATH, 'avatars')
  AVATARS_SIZE_TUPLE = (30, 100, 200)

  MAIL_SERVER = os.getenv('MAIL_SERVER')
  MAIL_PORT = 465
  MAIL_USE_SSL = True
  MAIL_USERNAME = os.getenv('MAIL_USERNAME')
  MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
  MAIL_DEFAULT_SENDER = ('Albumy Admin', MAIL_USERNAME)

class DevelopmentConfig(BaseConfig):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = db_url
  
class TestingConfig(BaseConfig):
  TESTING = True
  WTF_CSRF_ENABLED = False
  SQLALCHEMY_DATABASE_URI = db_url

class ProductionConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI = db_url


config = {
  'development': DevelopmentConfig,
  'testing': TestingConfig,
  'production': ProductionConfig
}