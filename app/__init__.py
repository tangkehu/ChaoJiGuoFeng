
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
    register_command(app)

    @app.context_processor  # Flask的上下文处理器，向模板的上下文插入新变量（可以是值和函数）
    def inject_context():
        def truncate_self(string, length):
            _str = str(string)
            if _str.__len__() >= int(length):
                _str = _str[:int(length)] + '...'
            return _str
        return dict(BOOT_CDN=app.config['BOOT_CDN'], truncate_self=truncate_self)

    from .main import main_bp
    app.register_blueprint(main_bp)
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    from .manage import manage_bp
    app.register_blueprint(manage_bp, url_prefix='/manage')

    from . import models  # 导入数据模型，否则无法创建数据表

    return app


def register_command(app):
    @app.cli.command()  # Flask的命令行命令注册器，类似flask run
    @click.option('--email', help='邮箱')
    @click.option('--password', help='密码')
    @click.option('--username', default='系统管理员', help='用户名')
    def register_user(email, password, username):
        """ 注册用户 """
        from .models import User
        flg = User().update(email=email, password=password, username=username)
        click.echo('email: {}  password: {}  username: {}'.format(email, password, username))
        click.echo('注册成功' if flg else '注册失败')

    @app.cli.command()
    @click.option('--email', help='邮箱')
    @click.option('--password', help='密码')
    def change_pass(email, password):
        """ 修改用户密码 """
        click.echo('email: {}  password: {}'.format(email, password))
        from .models import User
        user_ = User.query.filter_by(email=email).first()
        if user_:
            flg = user_.update(email=email, password=password)
            click.echo('修改密码成功' if flg else '修改密码失败')
        else:
            click.echo('不存在该用户')

    @app.cli.command()
    @click.option('--email', help='邮箱')
    def remove_user(email):
        """ 移除用户 """
        click.echo('email: {}'.format(email))
        from .models import User
        user_ = User.query.filter_by(email=email).first()
        if user_:
            user_.remove()
            click.echo('用户移除成功')
        else:
            click.echo('不存在该用户')


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
