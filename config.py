# -*- coding: utf-8 -*-
import os


class Config:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    SECRET_KEY = 'you will not guess it'
    BABEL_DEFAULT_LOCALE = 'zh_CN'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:password@localhost/test"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/db'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/db'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
