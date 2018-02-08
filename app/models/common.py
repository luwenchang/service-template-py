# -*- coding: utf-8 -*-
__author__ = 'vincent'

import simplejson as json
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils import toolkit


'''
# 用户模型必须实现 82页：表8-1 所需要的四个方法，如下：
# is_authenticated 如果用户已登录，则返回True，否则返回False
# is_active 如果允许用户登录，则返回True，否则返回False
# is_anonymous 对普通用户必须返回False
# get_id 必须返回用户的唯一标示符，使用unicode 编码字符串
可以使用 Flask-Login 提供的UserMixin类，就自动拥有以上四种方法了
'''
from flask_login import UserMixin
from flask_login import AnonymousUserMixin

# 下面这个包 itsdangerous 用于生成确认令牌
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask import request
from flask import url_for

from sqlalchemy.sql import and_
from sqlalchemy.sql import or_
from sqlalchemy.dialects.mysql import TINYINT
from .. import Cfg


from .. import db
from datetime import datetime
import time


#
# class TableBase:
#     # 所有表公共字段
#     # seq = db.Column(db.Integer, autoincrement=True)
#
#     # createTimestamp = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))
#     # updateTimestamp = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
#
#     # # 此种方式（快捷自动更新时间的方式 是输入 mysql 的特有功能，其他数据库引擎不支持，特此注释）
#     # create_timestamp = db.Column(db.TIMESTAMP(True), nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))
#     # update_timestamp = db.Column(db.TIMESTAMP(True), nullable=False, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
#
#     # create_timestamp = db.Column(db.TIMESTAMP(True), nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))
#     # # 注意，此种方式，则后续需要程序对该字段值进行更新
#     # update_timestamp = db.Column(db.TIMESTAMP(True), nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))
#
#     # 允许展示的字段列表
#     _to_dict_default_fields_ = []
#
#     def to_dict(self, fields=[]):
#         info = toolkit.filter_table_field(self.__dict__, fields if fields else self._to_dict_default_fields_)
#         return json.loads(json.dumps(info, default=toolkit.json_serial))



class TableBase:
    # 所有表公共字段
    seq = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_timestamp = db.Column(db.TIMESTAMP, index=True, server_default=db.text("CURRENT_TIMESTAMP"))
    update_timestamp = db.Column(db.TIMESTAMP, index=True,
                                 server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # if current_app.config.SQLALCHEMY_DATABASE_URI.startswith('mysql'):
    #     update_timestamp = db.Column(db.BigInteger, index=True, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    # else:
    #     update_timestamp = db.Column(db.BigInteger, index=True, onupdate=db.text('CURRENT_TIMESTAMP'))

    # 允许展示的字段列表
    _to_dict_default_fields_ = []

    def to_dict(self, fields=[]):
        info = toolkit.filter_table_field(self.__dict__, fields if fields else self._to_dict_default_fields_)
        return json.loads(json.dumps(info, default=toolkit.json_serial))

