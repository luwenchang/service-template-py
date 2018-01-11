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
from . import logger

from ..utils import token_help
from app.utils import exceptions


reload(sys)
sys.setdefaultencoding("utf-8")


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(login_tag_account, password):
    '''验证用户密码'''
    # Token
    token = request.headers.get("X-Auth-Token")
    if token:
        # 此时属于验证token
        kvs = token_help.get_token_cache('auth:token:{}'.format(token))

        # 不存在该Token
        if not kvs:
            logger.error("当前Token已失效或不存在")
            return False
        user = json.loads(kvs.get('user'))

        g.token_used = True
        # 记录当前Token值
        g.current_token = token
        # g.current_user = User.query.filter_by(id=user_id).first()
        g.current_user = user
        return True

    else:
        # 获取 Body 数据
        body = request.get_json()
        # 验证 用户名密码
        if not body:
            logger.error("缺少请求参数体")
            return False

        # 实验室 ID
        lab_id = body.get('lab_id')
        # 用户名
        account = body.get('account')
        # 密码
        password = body.get('password')

        # 此时属于验证 用户名/密码
        if not lab_id or  not account or  not password:
            # 实验室ID 和 用户名  和 密码不能为空
            logger.error("认证参数缺失")
            return False

        # 查找用户信息
        user = User.query.filter(
            and_(
                User.internalUserId == lab_id,
                or_(
                    User.username == account,
                    User.mobile == account,
                    User.email == account
                )
            )
        ).first()
        if not user:
            # 未找到指定用户
            g.current_user = None
            return False

        if not user.verify_password(password):
            # 密码错误
            g.current_user = None
            logger.error("密码错误验证失败")
            return False

        g.token_used = False
        g.current_token = None
        cur_user = user.to_dict()
        g.current_user = {
            'id' : cur_user['id'],
            'internalUserId' : cur_user['internalUserId'],
            'groupId' : cur_user['groupId'],
            'isLabUser' : cur_user['isLabUser'],
            'isIndependent' : cur_user['isIndependent'],
            'noBalanceQuota' : cur_user['noBalanceQuota'],
            'isDisabled' : cur_user['isDisabled'],
        }

    return True




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


# 通过如下方法，api 蓝本中所有路由都能进行自动认证。
# 而且作为附加认证，before_request 处理程序还会拒绝已通过认证，但没有确认账户的用户
@api_bp.before_request
@create_request_id
@auth.login_required
def before_request():

    if not g.current_user:
        logger.warning(str(exceptions.LoginFailed()))
        return exceptions.LoginFailed().dict

    elif g.current_user.get('isDisabled'):
        logger.warning(str(exceptions.AccountDisabled()))
        return exceptions.AccountDisabled().dict
    else:
        logger.info('权限验证成功')
    # 默认提取请求体
    g.json_data = request.get_json()





@api_bp.after_request
def af_request(response):
    data = json.loads(response.get_data())
    if not data.get('RequestID'):
        data['RequestID'] = g.request_id
    data = jsonify(data).get_data()
    response.set_data(data)
    return response


