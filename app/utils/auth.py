# -*- coding: utf-8 -*-
__author__ = 'vincent'


import sys
import hashlib
import uuid
from flask import current_app

# 下面这个包 itsdangerous 用于生成确认令牌
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def str_encrypt(str):
    """
    使用sha1加密算法，返回str加密后的字符串
    """
    sha = hashlib.sha1(str)
    encrypts = sha.hexdigest()
    return encrypts

def get_salted_password_hash(salt, password, secret):
    """
    根据密码及相关信息获取加密后的摘要
    :param salt:
    :param password:
    :param secret:
    :return:
    """
    str_to_hash = '~{0}~{1}~{2}~'.format(salt, password, secret)
    hash = str_encrypt(str_to_hash)
    return hash

def get_password_md5(password):
    """通过MD5加密密码"""
    m2=hashlib.md5()
    m2.update(password)
    return m2.hexdigest()


# def generate_token(data, expiration=3600):
#     '''生成一个令牌'''
#     s = Serializer(current_app.config['TOKEN_SECRET_KEY'], expiration)
#     # return s.dumps({'confirm': self.users_id})
#     return s.dumps(data)
#
# def confirm_token(token):
#     '''认证令牌，并返回令牌中存储的数据'''
#     s = Serializer(current_app.config['TOKEN_SECRET_KEY'])
#     try:
#         data = s.loads(token)
#     except:
#         return False
#     return data