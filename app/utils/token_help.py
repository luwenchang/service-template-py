# -*- coding: utf-8 -*-
__author__ = 'vincent'

import uuid
import json
from redis_help import redis_client

from werkzeug.security import generate_password_hash, check_password_hash
from . import redis_help

# 下面这个包 itsdangerous 用于生成确认令牌
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



def generate_auth_token(secret_key, user_id, expire=3600):
    '''使用编码后的用户ID字段值生成一个签名令牌，指定以秒为单位的过期时间'''
    s = Serializer(secret_key, expires_in=expire)
    # 设置Token值
    token = s.dumps({'id': user_id, 'xid': uuid.uuid4().hex})
    return token



def verify_auth_token(secret_key, token):
    '''解码用户令牌，如果解码成功且可用，则返回对应用户ID'''
    s = Serializer(secret_key)
    try:
        data = s.loads(token)
    except:
        return None

    return redis_help.get('auth:token:{}'.format(data))


def set_token_cache(key, expire, **kwargs):
    '''以管道方式批量执行命令，以哈希表方式存储 Token相关信息数据, kvs 是以一级结构存在的 k-v 值，v为字符串'''
    # 创建一个 redis的管道命令对象
    pipeline = redis_client.pipeline()
    pipeline.hmset(key, kwargs)
    pipeline.expire(key, expire)
    pipeline.execute()


def get_token_cache(key):
    '''获取缓存的 token 相关数据信息'''
    kvs = redis_client.hgetall(key)
    if not kvs: return None
    return kvs


def delete_token_cache(key):
    '''删除缓存的 token 相关数据信息'''
    redis_client.delete(key)

