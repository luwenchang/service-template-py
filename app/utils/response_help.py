# -*- coding: utf-8 -*-
__author__ = 'vincent'
from flask import Flask, Response, jsonify


# 增加了Response 类 对 dict 和 list 类型数据的处理
class MyResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (list, dict)):
            response = jsonify(response)
        return super(Response, cls).force_type(response, environ)