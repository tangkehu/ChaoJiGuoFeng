
from flask import render_template

from . import manage_bp


@manage_bp.route('/news')
def news():
    return render_template('manage/news.html')


@manage_bp.route('/activities')
def activities():
    return render_template('manage/news.html')


@manage_bp.route('/works')
def works():
    return render_template('manage/news.html')


@manage_bp.route('/products')
def products():
    return render_template('manage/news.html')


@manage_bp.route('/indent')
def indent():
    return render_template('manage/news.html')


@manage_bp.route('/about')
def about():
    return render_template('manage/news.html')
