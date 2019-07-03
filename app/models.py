
import os
from datetime import datetime
from flask import current_app
from app import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Boolean, default=False)
    title = db.Column(db.String(64))
    summary = db.Column(db.String(128))
    content = db.Column(db.Text)
    cover = db.Column(db.String(128), default='/static/img/logo.gif')
    type = db.Column(db.Integer)

    entry = db.relationship('Entry', backref='article', lazy='dynamic')

    def update(self, a_type, **kwargs):
        """  用于更新数据，必需文章类型a_type，可自定义cover封面图，否则默认文章第一张图。 """
        import re
        self.datetime = datetime.now()
        self.title = kwargs['title'].strip() if kwargs.get('title') else self.title
        self.summary = kwargs['summary'].strip() if kwargs.get('summary') else self.summary
        self.content = kwargs['content'] if kwargs.get('content') else self.content
        img_urls = re.findall(r'src="(.*?)"', self.content)
        self.cover = kwargs['cover'] if kwargs.get('cover') else img_urls[0] if img_urls else self.cover
        self.type = int(a_type)
        db.session.add(self)
        db.session.commit()

    def alter_status(self):
        self.status = False if self.status else True
        db.session.add(self)
        db.session.commit()

    def remove(self):
        """ 删除时删除储存在本地的图片文件 """
        import re
        img_urls = re.findall(r'src="/static/article-img/(.*?)"', self.content)
        try:
            for item in img_urls:
                os.remove(os.path.join(current_app.config['ARTICLE_PATH'], item))
        except Exception as e:
            current_app.logger.info(str(e))
        for item in self.entry.all():
            # 若存在活动报名表则删除活动报名
            item.remove()
        db.session.delete(self)
        db.session.commit()


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Boolean, default=False)
    title = db.Column(db.String(64))
    url = db.Column(db.String(128))


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Boolean, default=False)
    title = db.Column(db.String(64))
    price = db.Column(db.Float)
    url = db.Column(db.String(128))

    indent = db.relationship('Indent', backref='products', lazy='dynamic')


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.now)
    name = db.Column(db.String(32))
    contacts = db.Column(db.String(32))
    remarks = db.Column(db.String(128))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

    def update(self, aid, **kwargs):
        if kwargs.get('name') and kwargs.get('contacts') and Entry.query.filter(
            Entry.id != self.id,
            Entry.article_id == aid,
            Entry.name == kwargs['name'].strip(),
            Entry.contacts == kwargs['contacts'].strip()
        ).first():
            return False
        self.datetime = datetime.now()
        self.name = kwargs['name'].strip() if kwargs.get('name') else self.name
        self.contacts = kwargs['contacts'].strip() if kwargs.get('contacts') else self.contacts
        self.remarks = kwargs['remarks'].strip() if kwargs.get('remarks') else self.remarks
        self.article = Article.query.get_or_404(int(aid))
        db.session.add(self)
        db.session.commit()
        return True

    def remove(self):
        db.session.delete(self)
        db.session.commit()


class Indent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.now)
    name = db.Column(db.String(32))
    contacts = db.Column(db.String(32))
    address = db.Column(db.String(128))
    remarks = db.Column(db.String(128))
    count = db.Column(db.Integer, default=1)
    total = db.Column(db.Float)
    pay_status = db.Column(db.Boolean, default=False)
    send_status = db.Column(db.Boolean, default=False)
    products_id = db.Column(db.Integer, db.ForeignKey('products.id'))
