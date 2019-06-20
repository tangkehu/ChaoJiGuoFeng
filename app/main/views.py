
from flask import render_template, jsonify, url_for

from . import main_bp


@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/news')
def news():
    return render_template('main/news.html')


@main_bp.route('/news_content/<int:page>')
def news_content(page):
    content_list = ''
    return jsonify({'content': render_template('main/news_content.html', content_list=content_list),
                    'next_url': url_for('.news_content', page=page+1)})


@main_bp.route('/activities')
def activities():
    return render_template('main/activities.html')


@main_bp.route('/works')
def works():
    return render_template('main/works.html')


@main_bp.route('/products')
def products():
    return render_template('main/products.html')


@main_bp.route('/about')
def about():
    return render_template('main/about.html')
