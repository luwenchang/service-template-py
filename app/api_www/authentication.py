# -*- coding: utf-8 -*-
__author__ = 'vincent'

import sys
import simplejson as json
from functools import wraps
import uuid
from flask import g, request, current_app
from flask import jsonify
from sqlalchemy.sql import or_
from sqlalchemy.sql import and_
from flask_httpauth import HTTPBasicAuth

from ..models.users import User

from . import api_bp
# from . import logger

from ..utils import token_help
from app.utils import exceptions


reload(sys)
sys.setdefaultencoding("utf-8")


auth = HTTPBasicAuth()

def verify_login_account_password(password, email=None, mobile=None):
    '''验证用户名密码方式登录的用户'''
    if email:
        u = User.query.filter_by(email=email).first()
    elif mobile:
        u = User.query.filter_by(mobile=mobile).first()
    else:
        current_app.logger.error('密码验证错误，缺少登录帐号')
        return False

    login_info = u.local_login.first()
    if not login_info.verify_password(password): return False

    g.current_user = u.to_dict()
    g.token_used = False
    return True


def verify_login_token(token):
    '''验证Token方式登录的用户'''
    # 缓存中的 token
    kvs = token_help.get_token_cache('auth:token:{}'.format(token))
    # 不存在该Token
    if not kvs:
        current_app.logger.error("当前Token已失效或不存在")
        return False
    # 存在Token，则取出对应用户
    user = json.loads(kvs.get('user'))

    g.token_used = True
    # 记录当前Token值
    g.current_token = token
    # g.current_user = User.query.filter_by(id=user_id).first()
    g.current_user = user
    return True


def verify_login_ak():
    '''验证ak方式登录用户的 请求签名'''
    pass


def get_json_body():
    try:
        # 获取 Body 数据
        body = request.get_json()
    except Exception, e:
        # current_app.logger.error('缺少请参数')
        body = {}

    return body



@auth.verify_password
def verify_password(login_tag_account, password):
    '''验证用户密码'''

    token = request.headers.get("X-Auth-Token")
    auth_type = request.headers.get("X-Auth-Type")

    if auth_type == 'email-password':
        return verify_login_account_password(email=login_tag_account, password=password)

    elif auth_type == 'mobile-password':
        return verify_login_account_password(mobile=login_tag_account, password=password)

    elif auth_type == 'ak':
        pass
        # return verify_login_ak()

    # elif auth_type == 'weibo-token':
    #     pass
    # elif auth_type == 'weixin-token':
    #     pass
    elif auth_type == 'token':
        return verify_login_token(token)


    return False




@auth.error_handler
def auth_error():
    return {
        "code" : "LoginField",
        "message" : "登陆验证失败"
    }


def create_request_id(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # 如果上下文中不存在 request_id， 则生成一个 request_id
        if not getattr(g, 'request_id', None):
            g.request_id = str(uuid.uuid4())

        g.logger_extra = {"RequestID": g.request_id}
        return f(*args, **kwargs)
    return decorated


# 通过如下方法，api 蓝本中所有路由都  先进行创建唯一请求ID
# 而且作为附加认证，before_request 处理程序还会拒绝已通过认证，但没有确认账户的用户
@api_bp.before_request
@create_request_id
def before_request():
    # 添加用户时未验证
    # TODO 实际应该在验证时判断 是否需要用户登录，例如注册用户，此处暂未处理
    if g.get('current_user'):
        if g.current_user.get('is_disabled'):
            current_app.logger.warning('当前用户被禁止登录')
            return exceptions.AccountDisabled().dict

    # 默认提取请求体
    g.json_data = get_json_body()




@api_bp.after_request
def af_request(response):
    data = json.loads(response.get_data())
    # 确保必然含有返回值
    if not data:
        data = {'RequestID' : g.request_id }
    else:
        if not data.get('RequestID'):
            data['RequestID'] = g.request_id

    data = jsonify(data).get_data()
    response.set_data(data)
    return response


