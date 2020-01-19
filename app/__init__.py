# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template
from flask_login import current_user
from flask_wtf.csrf import CSRFError
from app.blueprint.main import main_bp
from app.blueprint.auth import auth_bp
from app.extensions import bootstrap, db, login_manager, dropzone, mail, csrf, ext, avatars, migrate
from app.config import config
from app.command import register_commands

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    
    app = Flask('app')
    
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.config.from_object(config[config_name])

    register_blueprint(app)
    register_extensions(app)
    register_commands(app)
    register_errors(app)
    
    return app

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    dropzone.init_app(app)
    csrf.init_app(app)
    ext.init_app(app)
    avatars.init_app(app)
    migrate.init_app(app, db)

def register_blueprint(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400 
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('errors/413.html'), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 500
