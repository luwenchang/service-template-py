# -*- coding: utf-8 -*-
__author__ = 'vincent'

import json
from flask import jsonify, g, current_app
from flask_restful import Resource, reqparse, marshal_with, fields, marshal_with_field
from app.utils import token_help, redis_help, exceptions


# 舍弃 @marshal_with 方式原因是： 当根据请求解惑的不可用操作需要返回 错误数据时。返回值被强制更改了


class GetToken(Resource):
    def post(self):
        if g.token_used:
            current_app.logger.error('Token 登录用户禁止此项操作')
            return  exceptions.ForbiddenAction('Token 登录用户禁止此项操作').dict

        expiration = 3600
        token = token_help.generate_auth_token(
            current_app.config['SECRET_KEY'],
            user_id=g.current_user['id'],
            expire=expiration
        )
        # 根据Token值，设置缓存用户信息的Key
        key = 'auth:token:{}'.format(token)
        # 缓存 用户信息
        token_help.set_token_cache(key, expiration, user=json.dumps(g.current_user))
        current_app.logger.info('Token 获取成功')

        return {
                'token': token,
                'expiration': expiration
            }


# class DeleteToken(Resource):
#     def post(self):
#         if not g.token_used: return jsonify({"message" : "未制定待释放的Token，请以待释放Token请求"})
#
#         key = 'auth:token:{}'.format(g.currnet_token)
#         token_help.delete_token_cache(key)
#         current_app.logger.info('Token 当前用户的Token已删除')
#         return jsonify(
#             {
#                 'message': '当前用户Token已释放'
#             },
#             RequestId=g.request_id
#         )

