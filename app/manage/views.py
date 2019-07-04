
from flask import render_template, request, redirect, url_for, jsonify, current_app, abort

from app.utils import random_filename, resize_img
from app.models import Article, Entry, Video
from . import manage_bp


@manage_bp.route('/news')
def news():
    news_list = Article.query.filter_by(type=1).order_by(Article.datetime.desc()).all()
    return render_template('manage/news.html', news_list=news_list, page_name='最新动态')


@manage_bp.route('/activities')
def activities():
    activities_list = Article.query.filter_by(type=2).order_by(Article.datetime.desc()).all()
    return render_template('manage/activities.html', activities_list=activities_list, page_name='活动报名')


@manage_bp.route('/entry/<int:aid>')
def entry(aid):
    """ 报名管理页面 """
    activity_obj = Article.query.get_or_404(int(aid))
    return render_template('manage/entry.html', activity_obj=activity_obj, Entry=Entry)


@manage_bp.route('/entry/update/<int:aid>', methods=['GET', 'POST'])
@manage_bp.route('/entry/update/<int:aid>/<int:eid>', methods=['GET', 'POST'])
def entry_update(aid, eid=0):
    """ 报名信息新增和修改 """
    entry_obj = Entry.query.get_or_404(int(eid)) if eid else None
    if request.method == 'POST':
        if entry_obj:
            flg = entry_obj.update(aid, **request.form.to_dict())
        else:
            flg = Entry().update(aid, **request.form.to_dict())
        return '报名信息提交成功' if flg else '报名信息重复，请重试。'
    return render_template('manage/entry_update.html', entry_obj=entry_obj)


@manage_bp.route('/entry/remove', methods=['POST'])
def entry_remove():
    """ 报名信息移除 """
    Entry.query.get_or_404(int(request.form.get('eid'))).remove()
    return 'success'


@manage_bp.route('/works', methods=['GET', 'POST', 'DELETE'])
def works():
    """ 作品展示管理页面，作品发布，作品删除 """
    if request.method == 'POST':
        # 作品发布
        Video.query.get_or_404(int(request.form.get('vid'))).alter_status()
        return 'success'
    if request.method == 'DELETE':
        # 作品删除
        Video.query.get_or_404(int(request.form.get('vid'))).remove()
        return 'success'
    video_list = Video.query.order_by(Video.datetime.desc()).all()
    return render_template('manage/works.html', page_name='作品展示', video_list=video_list)


@manage_bp.route('/works/update/<string:url>', methods=['GET', 'POST'])
@manage_bp.route('/works/update/<string:url>/<int:vid>', methods=['GET', 'POST'])
def works_update(url, vid=None):
    """ 作品新增和修改 """
    url = url.replace('%2F', '/')
    video_obj = Video.query.get_or_404(int(vid)) if vid else None
    if request.method == 'POST':
        if video_obj:
            video_obj.update(url, request.form.get('title'))
        else:
            Video().update(url, request.form.get('title'))
        return redirect(url_for('.works'))
    return render_template('manage/works_update.html', video_obj=video_obj, url=url)


@manage_bp.route('/video', methods=['POST', 'DELETE'])
def video():
    """ 视频的上传和删除 """
    import os
    if request.method == 'POST':
        # 视频上传
        new_video = request.files.get('file')
        new_filename = random_filename(new_video.filename)
        new_video.save(os.path.join(current_app.config['VIDEO_PATH'], new_filename))
        return url_for('.works_update', url=url_for('static', filename='video/'+new_filename).replace('/', '%2F'))
    if request.method == 'DELETE':
        # 视频删除
        try:
            os.remove(os.path.join(current_app.config['VIDEO_PATH'], request.form.get('url').split('/')[-1]))
        except Exception as e:
            current_app.logger.info(str(e))
        return 'success'
    abort(404)


@manage_bp.route('/products')
def products():
    return render_template('manage/products.html', page_name='产品管理')


@manage_bp.route('/indent')
def indent():
    return render_template('manage/indent.html', page_name='订单管理')


@manage_bp.route('/about', methods=['GET', 'POST'])
def about():
    about_obj = Article.query.filter_by(type=3).first()
    if not about_obj:
        Article().update(3)
        about_obj = Article.query.filter_by(type=3).first()

    if request.method == 'POST':
        about_obj.update(3, **request.form.to_dict())
        return 'success'

    return render_template('manage/about.html', page_name='关于我们', about_obj=about_obj)


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
