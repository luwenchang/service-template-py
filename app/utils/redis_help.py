# -*- coding: utf-8 -*-


from app import Cfg
import simplejson as json
import redis
import time
import random
import datetime

from .toolkit import json_dumps

redis_option = {
    'host'    : Cfg['redis'].get('host', '127.0.0.1'),
    'port'    : Cfg['redis'].get('port', 6379),
    'db'      : Cfg['redis'].get('db', 0),
    'password': Cfg['redis'].get('password', None),
}

redis_client = redis.Redis(**redis_option)


def get(key):
    '''根据Key值 获取Value，如果Value可转化为Dict或/List 则进行转化，否则直接返回字串,如果为空，则返回None'''
    redis_result = redis_client.get(key)
    if isinstance(redis_result, (str, unicode)):
        try:
            redis_result = json.loads(redis_result)
        except Exception as e:
            pass
    return redis_result

def set(key, value, expire=None):
    '''设置key'''
    if not isinstance(value, str):
        value = json_dumps(value)

    if isinstance(expire, int):
        redis_client.setex(key, value, expire)

    elif isinstance(expire, datetime.datetime):
        redis_client.set(key, value)
        redis_client.expireat(key, expire)

    else:
        redis_client.set(key, value)


def delete(key):
    '''删除指定key'''
    redis_client.delete(key)

def patten_delete(patten):
    '''清除现存的所有keys'''
    matched_keys = redis_client.keys(patten)
    for key in matched_keys:
        delete(key)
