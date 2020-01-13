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

  APP_PER_PAGE = 20
  APP_DETAILS_PER_PAGE = 16
  ALBUMY_MAIL_SUBJECT_PREFIX = '[Albumy]'
  ALBUMY_ADMIN_EMAIL = os.getenv('ALBUMY_ADMIN', 'admin@helloflask.com')

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