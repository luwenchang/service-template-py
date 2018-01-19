# -*- coding: utf-8 -*-
__author__ = 'vincent'


from flask import jsonify, g, current_app, request
from flask_restful import Resource, reqparse, marshal_with, marshal_with_field


from app.utils import token_help, redis_help, toolkit

from app.models.users import User

from app import db


from app.utils import exceptions
from app.utils.validator import check_body
from app import BodySchema

# User API 返回数据参数处理
_response_fields = ['id', 'nickname', 'email', 'mobile', 'note', 'name', 'intro',
                  'head_portrait', 'is_disabled', 'create_timestamp']


class GetUser(Resource):
    def post(self):
        user = User.query.filter_by(id=g.current_user['id']).first()

        current_app.logger.info('已获取用户信息')
        return {
            "User" : user.to_dict(_response_fields)
        }


class SetUser(Resource):

    @check_body('user.SetUser')
    def post(self):

        user = User.query.filter_by(id=g.current_user['id']).first()
        args = g.json_data

        if args.get('nickname'):
            user.email = args.get('nickname')

        if args.get('email'):
            user.email = args.get('email')

        if args.get('mobile'):
            user.mobile = args.get('mobile')


        if args.get('note'):
            user.note = args.get('note')


        if args.get('name'):
            user.name = args.get('name')


        if args.get('intro'):
            user.intro = args.get('intro')

        if args.get('head_portrait'):
            user.head_portrait = args.get('head_portrait')


        db.session.add(user)
        db.session.commit()

        return {}
