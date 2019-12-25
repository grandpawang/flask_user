import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # init file upload
    # UPLOAD_FOLDER = r'temp/file/'
    # LOGS_FILE = r'temp/logs/app.log'
    # init secret key
    SECRET_KEY = '1e3df42bbfe146c785f422611d6e7429'
    # init item page
    ITEMS_PER_PAGE = 1
    # init json web token
    JWT_SECRET_KEY = SECRET_KEY
    JWT_AUTH_URL_RULE = '/login'
    JWT_EXPIRATION_DELTA = datetime.timedelta(3600)  # 60s *60 = 1h JWT_DEFAULT_REALM
    TEMPLATES_AUTO_RELOAD = True
    # init orm:sqlalchemy
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWD = '1234'
    DB_DATABASE = 'manage'
    # connect object
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWD}@{DB_HOST}/{DB_DATABASE}?charset=utf8'
    # 每次请求结束时自动commit数据库修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 如果设置成 True，SQLAlchemy将会记录所有发到标准输出(stderr)的语句,这对调试很有帮助.
    SQLALCHEMY_ECHO = False
    # 可以用于显式地禁用或者启用查询记录。查询记录 在调试或者测试模式下自动启用。
    SQLALCHEMY_RECORD_QUERIES = False
    # 数据库连接池的大小。默认是数据库引擎的默认值(通常是 5)。
    SQLALCHEMY_POOL_SIZE = 5
    # 指定数据库连接池的超时时间。默认是 10。
    SQLALCHEMY_POOL_TIMEOUT = 10
    # init cache redis
    # CACHE_TYPE = 'redis'
    # CACHE_REDIS_HOST = 'localhost'
    # CACHE_REDIS_PORT = 6379
    # CACHE_REDIS_DB = ''
    # CACHE_REDIS_PASSWORD = ''

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    PRODUCTION = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
