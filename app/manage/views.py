
import re
from flask import render_template, request, redirect, url_for, jsonify

from app.utils import random_filename, resize_img
from . import manage_bp


@manage_bp.route('/news')
def news():
    news_list = []
    for item in range(20):
        news_list.append({
            'id': item + 1,
            'status': True,
            'datetime': '2019-06-18 17:00:00',
            'title': '武侯祠旁读《蜀相》，这一次诵读如此美妙',
            'summary': '不要以为孩子们静不下来，在精心制作的冥想音乐中，他们如此专心专注，甚至像个小菩萨，内心是安定的，缓缓的告别浮躁，找寻自我心底的宁静。'
        })
    return render_template('manage/news.html', news_list=news_list, page_name='最新动态')


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


@manage_bp.route('/article/<int:tid>', methods=['GET', 'POST'])
@manage_bp.route('/article/<int:tid>/<int:aid>', methods=['GET', 'POST'])
def article(tid=1, aid=0):
    if request.method == 'POST':
        print(re.findall(r'src="(.*?)"', request.form.to_dict().get('content')))
        return redirect(url_for('.news') if tid == 1 else url_for('.activities'))
    return render_template('manage/article.html')


@manage_bp.route('/article/upload', methods=['POST'])
def article_upload():
    article_file = request.files.get('upload')
    filepath = 'app/static/article-img/'
    filename = resize_img(filepath, random_filename(article_file.filename), 600, article_file, True)
    return jsonify({'uploaded': True, 'url': url_for('static', filename='article-img/'+filename)})
