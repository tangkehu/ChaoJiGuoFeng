
from flask import render_template

from . import main_bp


@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/news')
def news():
    return render_template('main/news.html')


# @main_bp.route('/activities')
# def activities():
#     return render_template('')
#
#
# @main_bp.route('/works')
# def works():
#     return render_template('')
#
#
# @main_bp.route('/products')
# def products():
#     return render_template('')
#
#
# @main_bp.route('/about')
# def about():
#     return render_template('')
