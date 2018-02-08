# -*- coding: utf-8 -*-
__author__ = 'vincent'

import uuid

from flask import jsonify, g, current_app, request
from flask_restful import Resource, reqparse, marshal_with, marshal_with_field

from sqlalchemy import or_
from app.utils import token_help, redis_help, toolkit

from app.models.users import User, UserLocalAuth

from app import db
from ..authentication import auth

from app.utils import exceptions
from app.utils.validator import check_body
from app import BodySchema

# User API 返回数据参数处理
# _response_fields = ['id', 'nickname', 'email', 'mobile', 'note', 'name', 'intro',
#                   'head_portrait', 'is_disabled', 'create_timestamp']





class AddUser(Resource):

    @check_body('user.AddUser')
    def post(self):
        '''添加用户'''

        # 先提取待更新的参数
        u = User.query.filter(
            or_(
                User.nickname == g.json_data.get('nickname'),
                User.email == g.json_data.get('email'),
                User.mobile == g.json_data.get('mobile')
            )
        ).first()

        # 如果存在 u, 则表明用户已存在
        if u:
            if u.nickname == g.json_data.get('nickname'):
                log = '用户昵称已存在'
            elif u.email == g.json_data.get('email'):
                log = '该邮件已注册'
            else:
                log = '该手机号已注册'

            current_app.logger.info(log)
            return exceptions.UserAlreadyExists(log).dict


        u = User(
            id = uuid.uuid4().hex,
            nickname = g.json_data.get('nickname'),
            email = g.json_data.get('email'),
            mobile = g.json_data.get('mobile'),
            note = g.json_data.get('note'),
            name = g.json_data.get('name'),
            intro = g.json_data.get('intro'),
            head_portrait = g.json_data.get('head_portrait'),
        )


        ul = UserLocalAuth(user_id=u.id, xname=uuid.uuid4().hex, password=g.json_data.get('password'))
        try:
            db.session.add_all([u, ul])
            db.session.commit()

            return
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('添加用户失败，报错详情: {}'.format(str(e)))
            return exceptions.UserAddedFailed('用户添加失败').dict



class GetUser(Resource):
    @auth.login_required
    def post(self):
        user = User.query.filter_by(id=g.current_user['id']).first()

        current_app.logger.info('已获取用户信息')
        return {
            "User" : user.to_dict()
        }


class SetUser(Resource):
    @auth.login_required
    @check_body('user.SetUser')
    def post(self):

        # 先提取待更新的参数
        update_info = []

        for k, v in g.json_data.items():
            if k in ['nickname', 'email', 'mobile']:
                update_info.append(User.__getattribute__(k) == v)

        u = User.query.filter(or_(*update_info)).all()

        # 对于已存在的值，则进行报错处理
        if not u:
            return exceptions.ParamsError('nickname / email / mobile 已存在').dict

        # 获取当前用户对象
        user = User.query.filter_by(id=g.current_user['id']).first()
        for k, v in g.json_data.items():
            if k in ['nickname', 'email', 'mobile', 'note', 'name', 'intro', 'head_portrait']:
                user.__setattr__(k, v)

        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(id=g.current_user['id']).first()

        return {
            "User" : user.to_dict()
        }
