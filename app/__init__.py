# -*- coding: utf-8 -*-
__author__ = 'vincent'

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy


from configs.config import Cfg
from configs.config import Config, TestConfig
from configs.config import BodySchema
from utils.response_help import MyResponse




db = SQLAlchemy()


def create_app(default_config_name):
    app = Flask(__name__)
    if default_config_name == 'TestConfig':
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(Config)
    # 解决
    app.response_class = MyResponse


    Config.init_app(app)

    # app 初始化 db
    db.init_app(app)

    # 注册蓝本 main
    from .api_www import api_bp as api_www_v1
    app.register_blueprint(api_www_v1, url_prefix='/wwwapi/v1')




    # 附加路由和自定义页面
    return app


