# -*- coding: utf-8 -*-
__author__ = 'vincent'


from flask import jsonify, g, current_app, request
from flask_restful import Resource, reqparse, marshal_with, marshal_with_field


from app.utils import token_help, redis_help, toolkit

from app.models.users import User

from app import db

from .. import logger

from app.utils import exceptions
from app.utils.validator import check_body
from app import BodySchema

# User API 返回数据参数处理
_response_fields = ['id', 'internalUserId', 'labUserSignInToken', 'avatarFileURL', 'username', 'email', 'mobile',
                  'note', 'name', 'company', 'locale', 'position', 'intro', 'groupId',
                  'lastSignInTime', 'lastSeenTime', 'isLabUser', 'isIndependent', 'noBalanceQuota',
                  'labUserBalanceQuota', 'isDisabled', 'cache_labUserBalance',
                  'createTimestamp']


class GetUser(Resource):
    def post(self):
        # if id != g.current_user['id']:
        #     logger.error("无效的请求，禁止非法获取用其他用户信息")
        #     return exceptions.InvalidRequest("无效的请求，禁止非法获取用其他用户信息").dict

        user = User.query.filter_by(id=g.current_user['id']).first()

        logger.info('已获取用户信息')
        return {
            "User" : user.to_dict(_response_fields)
        }




class SetUser(Resource):
    def post(self):

        args = check_body(request.get_json(), BodySchema['user']['SetUser'])

        user = User.query.filter_by(id=g.current_user['id']).first()

        if args.get('email'):
            user.email = args.get('email')

        if args.get('mobile'):
            user.mobile = args.get('mobile')

        if args.get('avatarFileURL'):
            user.avatarFileURL = args.get('avatarFileURL')

        if args.get('note'):
            user.note = args.get('note')

        if args.get('company'):
            user.company = args.get('company')

        if args.get('intro'):
            user.intro = args.get('intro')

        db.session.add(user)
        db.session.commit()

        return {
            "User" : user.to_dict(_response_fields)
        }
