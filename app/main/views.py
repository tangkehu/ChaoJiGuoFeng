
from flask import render_template, jsonify, url_for, request

from . import main_bp


@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/news')
def news():
    return render_template('main/news.html')


@main_bp.route('/news_content/<int:page>')
def news_content(page):
    content_list = []
    for item in range(4):
        content_list.append({'img': url_for('static', filename='img/dt.jpg'),
                             'title': '武侯祠旁读《蜀相》，这一次诵读如此美妙',
                             'info': url_for('.news_info', nid=0),
                             'content': '不要以为孩子们静不下来，在精心制作的冥想音乐中，他们如此专心专注，甚至像个小菩萨，内心是安定的，缓缓的告别浮躁，找寻自我心底的宁静。'})
    return jsonify({'content': render_template('main/news_content.html', content_list=content_list),
                    'next_url': url_for('.news_content', page=page+1) if page < 5 else ''})


@main_bp.route('/news_info/<int:nid>')
def news_info(nid):
    return render_template('main/news_info.html')


@main_bp.route('/activities')
def activities():
    return render_template('main/activities.html')


@main_bp.route('/activities_content/<int:page>')
def activities_content(page):
    content_list = []
    for item in range(4):
        content_list.append({'img': url_for('static', filename='img/hd.jpg'),
                             'title': '陪伴成长——妈妈的坚持，转移到孩子的坚持',
                             'info': url_for('.activities_info', aid=0),
                             'content': '亲子陪读有门道——挖掘中华经典的力量系列活动将于6月15日迎来第八期——陪伴成长——妈妈的坚持，转移到孩子的坚持，海光老师将与大家分享影响孩子坚持的几大因素。'})
    return jsonify({'content': render_template('main/activities_content.html', content_list=content_list),
                    'next_url': url_for('.activities_content', page=page+1) if page < 5 else ''})


@main_bp.route('/activities_info/<int:aid>', methods=['GET', 'POST'])
def activities_info(aid):
    if request.method == 'POST':
        print(request.form.to_dict())
        return '活动报名成功。'
    return render_template('main/activities_info.html')


@main_bp.route('/works')
def works():
    return render_template('main/works.html')


@main_bp.route('/works_content/<int:page>')
def works_content(page):
    content_list = []
    for item in range(2):
        content_list.append({'title': '国风作品展示-女生版VLOG展示',
                             'video': url_for('static', filename='video/zp.mp4')})
    return jsonify({'content': render_template('main/works_content.html', content_list=content_list),
                    'next_url': url_for('.works_content', page=page+1) if page < 5 else ''})


@main_bp.route('/products')
def products():
    return render_template('main/products.html')


@main_bp.route('/products_content/<int:page>')
def products_content(page):
    content_list = []
    for item in range(8):
        content_list.append({'img': url_for('static', filename='product/cp.png'),
                             'name': '经典论语著作，全本，诵读经典，提高诵读能力，提高国风能力',
                             'price': 99.9,
                             'info': url_for('.products_info', pid=0)})
    return jsonify({'content': render_template('main/products_content.html', content_list=content_list),
                    'next_url': url_for('.products_content', page=page+1) if page < 5 else ''})


@main_bp.route('/products_info/<int:pid>', methods=['GET', 'POST'])
def products_info(pid):
    if request.method == 'POST':
        print(request.form.to_dict())
        return '商品下单成功。'
    return render_template('main/products_info.html')


@main_bp.route('/about')
def about():
    return render_template('main/about.html')
