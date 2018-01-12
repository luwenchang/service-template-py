# -*- coding: utf-8 -*-

__author__ = 'vincent'

import os
import yaml
import json
from app.utils import toolkit

Cfg = {}
BodySchema = {}


# 获取当前目录
basedir = os.path.abspath(os.path.dirname(__file__))

# 加载 参数校验相关信息
with open(basedir + "/body-schema.yaml") as f:
    BodySchema = yaml.load(f)


with open(basedir + "/base-config.yaml") as f:
    Cfg = yaml.load(f)


SERVICE_CONFIG_PATH = os.environ.get('SERVICE_TEMPLATE_CONFIG_PATH')

with open(SERVICE_CONFIG_PATH) as f:
    _d = yaml.load(f)
    if _d:
        toolkit.obj_update(_d, Cfg)

class Config:
    DEBUG = True

    # 设置Logger的日志名称
    LOGGER_NAME = 'V'
    SECRET_KEY = Cfg.get('webServer', {}).get('secret')
    # 加盐加密字符串格式
    ENCRYPT_STR_FORMAT = Cfg.get('webServer', {}).get('str_format')
    # Token 的加密密匙
    TOKEN_SECRET_KEY= Cfg.get('webServer', {}).get('token_secret')

    # AK 加解密
    AES_KEY = Cfg.get('AES', {}).get('key')
    AES_IV = Cfg.get('AES', {}).get('iv')

    # 数据库连接池的大小。默认是数据库引擎的默认值 （通常是 5）
    SQLALCHEMY_POOL_SIZE = 5

    # 控制在连接池达到最大值后可以创建的连接数。当这些额外的 连接回收到连接池后将会被断开和抛弃。
    SQLALCHEMY_MAX_OVERFLOW = 10

    # 开启自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 避免内存开销太大，所以禁止此项,设置True;
    # 如果要开启慢查询，则此项需要设置 SQLALCHEMY_TRACK_MODIFICATIONS=False 并设置 SQLALCHEMY_RECORD_QUERIES=True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 开启慢查询
    SQLALCHEMY_RECORD_QUERIES = True

    # 分页中，每页默认现实的条目数量
    PER_PAGE = 20

    # SQL慢查询的阀值
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    # mysql 链接设置
    SQLALCHEMY_DATABASE_URI ="mysql://{}:{}@{}:{}/{}?charset=utf8".format(
        Cfg['mysql']['user'],
        Cfg['mysql']['password'],
        Cfg['mysql']['host'],
        Cfg['mysql']['port'],
        # Cfg['mysql']['database']
        'ast_test'
    )
    print SQLALCHEMY_DATABASE_URI

    # Redis 链接设置
    # REDIS_URL = "redis://localhost:6379/3"



    @staticmethod
    def init_app(app):
        pass



class TestConfig:
    # 设置Logger的日志名称
    LOGGER_NAME = 'VTest'
    SECRET_KEY = Cfg.get('webServer', {}).get('secret')
    # 加盐加密字符串格式
    ENCRYPT_STR_FORMAT = Cfg.get('webServer', {}).get('str_format')
    # Token 的加密密匙
    TOKEN_SECRET_KEY= Cfg.get('webServer', {}).get('token_secret')

    # AK 加解密
    AES_KEY = Cfg.get('AES', {}).get('key')
    AES_IV = Cfg.get('AES', {}).get('iv')

    # 数据库连接池的大小。默认是数据库引擎的默认值 （通常是 5）
    # SQLALCHEMY_POOL_SIZE = 5

    # 控制在连接池达到最大值后可以创建的连接数。当这些额外的 连接回收到连接池后将会被断开和抛弃。
    # SQLALCHEMY_MAX_OVERFLOW = 10

    # 开启自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 避免内存开销太大，所以禁止此项,设置True;
    # 如果要开启慢查询，则此项需要设置 SQLALCHEMY_TRACK_MODIFICATIONS=False 并设置 SQLALCHEMY_RECORD_QUERIES=True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 开启慢查询
    # SQLALCHEMY_RECORD_QUERIES = True

    # 分页中，每页默认现实的条目数量
    PER_PAGE = 20

    # SQL慢查询的阀值
    # FLASKY_SLOW_DB_QUERY_TIME = 0.5

    # mysql 链接设置
    SQLALCHEMY_DATABASE_URI ="mysql://{}:{}@{}:{}/{}?charset=utf8".format(
        Cfg['mysql']['user'],
        Cfg['mysql']['password'],
        Cfg['mysql']['host'],
        Cfg['mysql']['port'],
        'ast_test'
    )

    # 使用 sqlite 数据库
    # SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format( os.path.join(os.path.dirname(basedir), 'data-sqlite.db') )

    print SQLALCHEMY_DATABASE_URI

    # Redis 链接设置
    # REDIS_URL = "redis://localhost:6379/3"



    @staticmethod
    def init_app(app):
        pass
