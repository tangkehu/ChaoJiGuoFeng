
from flask import render_template, jsonify, url_for, request, current_app

from app.models import Article, Video, Products, Entry, Indent
from . import main_bp


@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/news')
def news():
    return render_template('main/news.html')


@main_bp.route('/news_content/<int:page>')
def news_content(page):
    pagination = Article.query.filter(Article.type == 1, Article.status == True).order_by(
        Article.datetime.desc()).paginate(page, current_app.config['PER_PAGE'], False)
    return jsonify({'content': render_template('main/news_content.html', content_list=list(pagination.items)),
                    'next_url': url_for('.news_content', page=pagination.next_num) if pagination.has_next else ''})


@main_bp.route('/news_info/<int:nid>')
def news_info(nid):
    news_obj = Article.query.get_or_404(int(nid))
    return render_template('main/news_info.html', news_obj=news_obj)


@main_bp.route('/activities')
def activities():
    return render_template('main/activities.html')


@main_bp.route('/activities_content/<int:page>')
def activities_content(page):
    pagination = Article.query.filter(Article.type == 2, Article.status == True).order_by(
        Article.datetime.desc()).paginate(page, current_app.config['PER_PAGE'], False)
    return jsonify({'content': render_template('main/activities_content.html', content_list=list(pagination.items)),
                    'next_url': url_for('.activities_content', page=pagination.next_num) if pagination.has_next else ''})


@main_bp.route('/activities_info/<int:aid>', methods=['GET', 'POST'])
def activities_info(aid):
    activities_obj = Article.query.get_or_404(int(aid))
    if request.method == 'POST':
        return '活动报名成功，请准时参加活动哟。' if Entry().update(aid, **request.form.to_dict()) else '你已报名成功，请勿重复报名。'
    return render_template('main/activities_info.html', activities_obj=activities_obj)


@main_bp.route('/works')
def works():
    return render_template('main/works.html')


@main_bp.route('/works_content/<int:page>')
def works_content(page):
    pagination = Video.query.filter(Video.status == True).order_by(Video.datetime.desc()).paginate(page, 3, False)
    return jsonify({'content': render_template('main/works_content.html', content_list=list(pagination.items)),
                    'next_url': url_for('.works_content', page=pagination.next_num) if pagination.has_next else ''})


@main_bp.route('/products')
def products():
    return render_template('main/products.html')


@main_bp.route('/products_content/<int:page>')
def products_content(page):
    pagination = Products.query.filter(Products.status == True, Products.is_remove == False).order_by(
        Products.datetime.desc()).paginate(page, 8, False)
    return jsonify({'content': render_template('main/products_content.html', content_list=list(pagination.items)),
                    'next_url': url_for('.products_content', page=pagination.next_num) if pagination.has_next else ''})


@main_bp.route('/products_info/<int:pid>', methods=['GET', 'POST'])
def products_info(pid):
    products_obj = Products.query.get_or_404(int(pid))
    if request.method == 'POST':
        Indent().update(pid, **request.form.to_dict())
        return '商品下单成功，请耐心等待我们与您联系。'
    return render_template('main/products_info.html', products_obj=products_obj)


@main_bp.route('/about')
def about():
    about_obj = Article.query.filter_by(type=3).first()
    return render_template('main/about.html', about_obj=about_obj)
