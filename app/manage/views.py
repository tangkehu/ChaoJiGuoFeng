
from flask import render_template

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
            'content': '不要以为孩子们静不下来，在精心制作的冥想音乐中，他们如此专心专注，甚至像个小菩萨，内心是安定的，缓缓的告别浮躁，找寻自我心底的宁静。'
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
