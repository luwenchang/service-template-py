# -*- coding: utf-8 -*-
__author__ = 'vincent'


import sys
import hashlib
import copy
from collections import OrderedDict
import simplejson as json
import datetime


def json_dumps(j, ensure_str=False):
    if (ensure_str is False) and (j is None):
        return None

    str_json = json.dumps(
            j,
            ensure_ascii=False,
            sort_keys=True,
            separators=(',', ':')).encode('utf8')
    return str_json


def get_str_md5(str):
    """通过MD5加密字符串"""
    m2=hashlib.md5()
    m2.update(str)
    return m2.hexdigest()

def str_encrypt(str):
    """
    使用sha1加密算法，返回str加密后的字符串
    """
    sha = hashlib.sha1(str)
    encrypts = sha.hexdigest()
    return encrypts

def get_salted_password_hash(salt, password, secret, str_format=''):
    """
    根据密码及相关信息获取加密后的摘要
    :param salt:
    :param password:
    :param secret:
    :return:
    """
    # str_to_hash = '~{0}~{1}~{2}~'.format(salt, password, secret)
    str_to_hash = str_format.format(salt, password, secret)
    hash = str_encrypt(str_to_hash)
    return hash


def obj_update(s, d):
    '''
    根据内容深度更新JSON对象

    参数
      s <JSON> 源JSON
      d <JSON> 目标JSON

    如：
      var s = { b: { c: 0 } };
      var d = { a: 9, b: { c: 9, d: 9 } };
      objUpdate(s, d)
      // d => { a: 9, b: { c: 0, d: 9 } }
    '''
    for k, v in s.items():
        if k not in d:
            d[k] = s[k]
        else:
            if isinstance(s[k], (dict, OrderedDict)):
                obj_update(s[k], d[k])
            else:
                d[k] = s[k]


def filter_table_field(source, fileds=[]):
    '''过滤表中的字段值，仅显示 fileds中展示的值'''
    new_source = {}
    source_keys = source.keys()
    for k in fileds:
        if k in source_keys:
            new_source[k] = source.get(k)
    return new_source


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    """
        >>> import json, datetime
        >>> a={'seq': 560L, 'lastSeenTime': datetime.datetime(2017, 11, 27, 3, 46, 54)}
        >>> print json.dumps(a, default=json_serial)
        >>> {"lastSeenTime": "2017-11-27 03:46:54", "seq": 560}
    """
    if isinstance(obj, (datetime.datetime, datetime.date)):
        # return obj.isoformat()
        return obj.strftime("%Y-%m-%d %H:%M:%S.%f")
    raise TypeError ("Type %s not serializable" % type(obj))



