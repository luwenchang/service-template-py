# -*- coding: utf-8 -*-
__author__ = 'vincent'
from flask import g

except_dict = {
    'LoginFailed': {"message" : "登录验证失败,请检查Token是否已过期，或用户名密码是否正确",},
    'NeedLogin': {'message': "当前请求需要先登陆"},
    'AccountDisabled': {'message': "帐号被禁用，请联系管理员"},
    'InvalidRequest' : {'message' : "无效的请求"},
    'ForbiddenAction' : {'message' : "禁止的操作"},
    'ParamsError' : {'message' : "参数错误"},
    'UserAlreadyExists' : {'message' : "当前用户已存在"},
    'UserAddedFailed' : {'message' : "当前用户已存在"}
}


def __init__(self, message=None,**kwargs):
    ''' make returned error message'''
    # 如果传入了 message 信息，则使用传入值，否则使用创建类时的默认值
    self.message = message if message else self.message
    self.dict = {
        "code" : self.__class__.__name__,
        "message" : self.message
    }


def __str__(self):
    return self.message


def __repr__(self):
    return  self.message



class IclException(Exception):
    pass



for (class_name, attr) in except_dict.items():
    # 动态类的创建方法
    # <类名> = type('<类名>', (新类的父类,), <新类中需要自定义的函数等等>)
    # Hello = type('Hello', (object,), dict(hello=fn)) # 创建Hello class
    eklass = type(
        str(class_name),  # 定义类名
        (IclException, ),  # 定义当前新类的 父类，需要用元组方式表示，且末尾需要添加逗号
        dict(__init__=__init__, __str__=__str__,  __repr__=__repr__, message=attr['message']) # 定义类的属性和方法
    )
    globals().update({class_name: eklass})  # 添加 globals 中

