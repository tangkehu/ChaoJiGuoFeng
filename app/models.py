
from datetime import datetime
from app import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Boolean, default=False)
    title = db.Column(db.String(64))
    summary = db.Column(db.String(128))
    content = db.Column(db.Text)
    cover = db.Column(db.String(128))
    type = db.Column(db.Integer)

    entry = db.relationship('Entry', backref='article', lazy='dynamic')


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
