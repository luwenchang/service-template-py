# -*- coding: utf-8 -*-
__author__ = 'vincent'

import unittest
import hashlib
import time
import re
import os
import json
from base64 import b64encode
from flask import url_for
from app import create_app, db
from app.models.users import User, UserLocalAuth
from app.utils.auth import get_password_md5
from tests.common import APITest

import forgery_py

from datetime import datetime
import uuid


class TokenAPITestCase(APITest):



    def test_add_user(self):
        '''验证批量添加用户是否成功'''
        count = 10
        u = User.query.all()
        c1 = len(u)
        self.add_users(count)

        u2 = User.query.all()
        self.assertTrue(c1+count ==len(u2))


    def test_check_user_password(self):
        '''验证新增用户的密码有效性'''
        self.add_users(10)
        user_list = User.query.all()
        u1 = user_list[0]

        u1_login_info = u1.local_login.first()
        self.assertTrue(u1_login_info.verify_password(get_password_md5(self.default_password)))
        self.assertFalse(u1_login_info.verify_password(get_password_md5('121212')))


    def test_user_reset_password(self):
        '''验证密码重置后的有效性'''
        user_list = self.add_users(1)
        u = User.query.filter_by(email=user_list[0].get('email')).first()

        login_info = u.local_login.first()
        # 验证原始密码 有效
        self.assertTrue(login_info.verify_password(get_password_md5(self.default_password)))

        # 重置用户密码
        login_info.reset_password(get_password_md5('12ABC'))
        db.session.add(login_info)

        # 验证新密码有效
        self.assertTrue(login_info.verify_password(get_password_md5('12ABC')))
        # 验证原密码无效
        self.assertFalse(login_info.verify_password(get_password_md5(self.default_password)))



    def test_user_delete(self):
        '''验证 删除用户的有效性'''
        self.add_users(10)

        user_list = User.query.all()

        u = user_list[8]

        u1 = User.query.filter_by(id=u.id).first()

        nickname = u1.nickname

        db.session.delete(u1)
        db.session.flush()

        new_user_list = User.query.filter_by(id=u.id).all()

        self.assertTrue(len(new_user_list) == 0)


    def test_user_set(self):
        '''验证 设置用户个人信息的有效性'''
        self.add_users(10)

        user_list = User.query.all()

        u = user_list[8]

        # 旧的用户信息
        old_info = u.to_dict()

        # 待更新的信息
        update_info = {
            'intro': forgery_py.currency.description(),
            'note': '{}x{}'.format(forgery_py.internet.user_name(), forgery_py.internet.cctld())
        }


        # 更新用户信息 SetUser
        response = self.client.post(
            '/wwwapi/v1/SetUser',
            headers=self.get_api_headers(auth_type='email-password', account=old_info.get('email'),
                                         password=get_password_md5(self.default_password)),
            data= json.dumps(update_info)
        )
        self.assertTrue(response.status_code == 200)

        # 重新获取用户信息
        response = self.client.post(
            '/wwwapi/v1/GetUser',
            headers=self.get_api_headers(auth_type='email-password', account=old_info.get('email'),
                                         password=get_password_md5(self.default_password))
        )
        self.assertTrue(response.status_code == 200)
        res = json.loads(response.data)
        for k, v in update_info.items():
            self.assertTrue(res.get('User', {}).get(k) == v)


    #
    #
    #     login_info = u.local_login.first()
    #     # 验证原始密码 有效
    #     self.assertTrue(login_info.verify_password(get_password_md5(u.nickname)))
    #
    #     # 重置用户密码
    #     login_info.reset_password(get_password_md5('12ABC'))
    #     db.session.add(login_info)
    #
    #     # 验证新密码有效
    #     self.assertTrue(login_info.verify_password(get_password_md5('12ABC')))
    #     # 验证原密码无效
    #     self.assertFalse(login_info.verify_password(get_password_md5(u.nickname)))
    #
    #
    #
    #
    #
    #
    # def test_get_token(self):
    #     '''验证获取 Token 是否成功'''
    #     self.add_users(10)
    #
    #     user_list = User.query.all()
    #     u = user_list[5]
    #
    #     # 验证密码错误的请求
    #     response = self.client.post(
    #         url_for('api_www.gettoken'),
    #         headers=self.get_api_headers(auth_type='email-password'  , account=u.email, password=get_password_md5(u.nickname))
    #     )
    #     self.assertTrue(response.status_code == 200)
    #
    #
    # def test_verify_token(self):
    #     '''验证 Token 的有效性'''
    #     self.add_users(10)
    #
    #     user_list = User.query.all()
    #
    #     u = user_list[5]
    #
    #     # 获取Token
    #     response = self.client.post(
    #         url_for('api_www.gettoken'),
    #         headers=self.get_api_headers(auth_type='email-password', account=u.email,
    #                                      password=get_password_md5(u.nickname))
    #     )
    #     self.assertTrue(response.status_code == 200)
    #     res = json.loads(response.data)
    #     token = res.get('token')
    #
    #
    #     # 通过获取 用户信息来验证 Token
    #     response = self.client.post(
    #         url_for('api_www.getuser'),
    #         headers=self.get_api_headers(auth_type='token', token=token)
    #     )
    #     self.assertTrue(response.status_code == 200)
    #     res = json.loads(response.data)
    #
    #     self.assertNotIn('code', res.keys())
    #     self.assertIn('User', res.keys())
