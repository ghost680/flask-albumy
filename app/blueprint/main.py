# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def main_index():
    print(request.remote_addr)
    print(request.user_agent.platform)
    print(request.user_agent.browser)
    print(request.user_agent.version)
    return render_template('main/index.html')