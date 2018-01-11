# -*- coding: utf-8 -*-
__author__ = 'vincent'

import sys
import time
import logging
import uuid
import flask
import functools
from collections import Hashable, Iterable, Mapping, Sequence
import re
import exceptions

from cerberus import Validator

from configs.config import BodySchema
from flask import g

class MyValidator(Validator):

    def _validate_type_email(self, value):
        """ 验证email类型"""
        pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        re_obj = re.compile(pattern)
        if re_obj.match(value):
            return True


    def _validate_islength(self, is_length, field, value):
        """
        注意，该规则的参数 is_length 将根据 注释中的 模式进行验证：
        (The rule's arguments are..... 这一行之后必须紧跟 is_length 的参数验证模式，
        或者该函数的注释直接写 is_length 的参数验证模式。可通过源码查看)
        The rule's arguments are validated against this schema:
        {'type': 'integer'}
        """
        if isinstance(value, Iterable) and len(value) != is_length:
            self._error(field, "Must be the specified length")


def check_body(schema_name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            # 提取指定校验参数模型
            tag_list = schema_name.split('.')
            schema = BodySchema.get(tag_list[0])
            for tag in tag_list[1:]:
                schema = schema.get(tag, {})

            # 获取待校验的参数数据
            document = {}
            document.update(kw)
            # request.body 中的数据默认覆盖 路由中的参数数据
            document.update(g.json_data)
            # 实例化校验器
            v = MyValidator(schema)
            # 允许未定义的参数通过验证
            v.allow_unknown = True
            if v.validate(document):
                return func(*args, **kw)
            else:
                return exceptions.ParamsError(v.errors).dict

        return wrapper
    return decorator