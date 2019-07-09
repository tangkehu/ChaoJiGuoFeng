
import os
import click
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config
from .utils import SSLSMTPHandler


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_message = '请先登录。'
login_manager.login_view = 'auth_bp.login'
login_manager.session_protection = 'strong'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    register_logging(app)
    register_errors(app)

    @app.context_processor  # Flask的上下文处理器，向模板的上下文插入新变量（可以是值和函数）
    def inject_context():
        def truncate_self(string, length):
            _str = str(string)
            if _str.__len__() >= int(length):
                _str = _str[:int(length)] + '...'
            return _str
        return dict(BOOT_CDN=app.config['BOOT_CDN'])

    @app.cli.command()  # Flask的命令行命令注册器，类似flask run
    def deploy():
        """ 用于部署的命令行命令 """
        click.echo('部署成功')

    from .main import main_bp
    app.register_blueprint(main_bp)
    from .manage import manage_bp
    app.register_blueprint(manage_bp, url_prefix='/manage')

    from . import models  # 导入数据模型，否则无法创建数据表

    return app


def register_errors(app):
    @app.errorhandler(403)
    def forbid_error(e):
        return render_template('exception.html'), 403

    @app.errorhandler(404)
    def not_found_error(e):
        return render_template('exception.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('exception.html'), 500


def register_logging(app):
    if not app.debug:
        if app.config.get('MAIL_SERVER'):
            mail_handler = SSLSMTPHandler(mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                                          credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']),
                                          fromaddr=app.config['MAIL_SENDER'], toaddrs=app.config['MAIL_ADMINS'],
                                          subject='超级国风WEB小程序 ERRORS 警报日志')
            mail_handler.setFormatter(logging.Formatter('''
                Message type:       %(levelname)s
                Location:           %(pathname)s:%(lineno)d
                Module:             %(module)s
                Function:           %(funcName)s
                Time:               %(asctime)s

                Message:

                %(message)s
                '''))
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/run.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
