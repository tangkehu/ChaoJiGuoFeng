
import os
from dotenv import load_dotenv


# 加载环境变量文件
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)


class Config:
    # 基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'set your secret key')
    PER_PAGE = 5
    ARTICLE_PATH = os.path.join(os.path.dirname(__file__), 'app'+os.sep+'static'+os.sep+'article-img')
    VIDEO_PATH = os.path.join(os.path.dirname(__file__), 'app'+os.sep+'static'+os.sep+'video')

    # CDN配置
    BOOT_CDN = True  # 是否使用免费快速的boot cdn服务

    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不追踪对象的修改，减少内存使用
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(
        os.getenv('DATABASE_USER'), os.getenv('DATABASE_PASS'), os.getenv('DATABASE_HOST'), os.getenv('DATABASE_NAME'))

    # 邮件配置
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_SENDER = 'www.chaojiguofeng.com <{}>'.format(MAIL_USERNAME)
    MAIL_ADMINS = ['329937872@qq.com']
