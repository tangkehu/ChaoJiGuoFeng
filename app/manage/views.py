
from flask import render_template, request, redirect, url_for, jsonify, current_app

from app.utils import random_filename, resize_img
from app.models import Article
from . import manage_bp


@manage_bp.route('/news')
def news():
    news_list = Article.query.filter_by(type=1).order_by(Article.datetime.desc()).all()
    return render_template('manage/news.html', news_list=news_list, page_name='最新动态')


@manage_bp.route('/activities')
def activities():
    activities_list = Article.query.filter_by(type=2).order_by(Article.datetime.desc()).all()
    return render_template('manage/activities.html', activities_list=activities_list, page_name='活动报名')


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


# -------------------- 图文文章的相关处理方法 --------------------------
@manage_bp.route('/article/<int:tid>', methods=['GET', 'POST'])
@manage_bp.route('/article/<int:tid>/<int:aid>', methods=['GET', 'POST'])
def article(tid, aid=0):
    """ 文章的新增和编辑 """
    article_obj = Article.query.get_or_404(int(aid)) if aid else None
    if request.method == 'POST':
        if article_obj:
            article_obj.update(tid, **request.form.to_dict())
        else:
            Article().update(tid, **request.form.to_dict())
        return redirect(url_for('.news') if tid == 1 else url_for('.activities'))
    return render_template('manage/article.html', article=article_obj, tid=tid)


@manage_bp.route('/article/upload', methods=['POST'])
def article_upload():
    """ 文章图片的保存 """
    article_file = request.files.get('upload')
    filename = resize_img(current_app.config['ARTICLE_PATH'], random_filename(article_file.filename),
                          600, article_file, True)
    return jsonify({'uploaded': True, 'url': url_for('static', filename='article-img/'+filename)})


@manage_bp.route('/article/publish', methods=['POST'])
def article_publish():
    """ 文章发布 """
    Article.query.get_or_404(int(request.form.get('aid'))).alter_status()
    return 'success'


@manage_bp.route('/article/remove', methods=['POST'])
def article_remove():
    """ 文章删除 """
    Article.query.get_or_404(int(request.form.get('aid'))).remove()
    return 'success'
