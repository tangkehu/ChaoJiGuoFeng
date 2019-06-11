
import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    @app.context_processor  # Flask的上下文处理器，向模板的上下文插入新变量（可以是值和函数）
    def inject_context():
        def test_def(num):
            return num+1
        return dict(BOOT_CDN=app.config['BOOT_CDN'], test_def=test_def)

    @app.cli.command()  # Flask的命令行命令注册器，类似flask run
    def deploy():
        """ 用于部署的命令行命令 """
        click.echo('部署成功')

    from .main import main_bp
    app.register_blueprint(main_bp)

    return app
