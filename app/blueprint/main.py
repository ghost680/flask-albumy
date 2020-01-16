# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request
from flask_login import login_required
from app.decorators import confirm_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def main_index():
    return render_template('main/index.html')

@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
@confirm_required
def main_upload():
    return render_template('main/index.html')