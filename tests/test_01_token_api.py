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


from datetime import datetime
import uuid


class TokenAPITestCase(APITest):


    def test_get_token(self):
        '''验证获取 Token 是否成功'''
        self.add_users(10)

        user_list = User.query.all()
        u = user_list[5]

        # 验证密码错误的请求
        response = self.client.post(
            '/wwwapi/v1/GetToken',
            headers=self.get_api_headers(auth_type='email-password'  , account=u.email, password=get_password_md5(self.default_password))
        )
        self.assertTrue(response.status_code == 200)


    def test_verify_token(self):
        '''验证 Token 的有效性'''
        self.add_users(10)

        user_list = User.query.all()

        u = user_list[5]

        # 获取Token
        response = self.client.post(
            '/wwwapi/v1/GetToken',
            headers=self.get_api_headers(auth_type='email-password', account=u.email,
                                         password=get_password_md5(self.default_password))
        )
        self.assertTrue(response.status_code == 200)
        res = json.loads(response.data)
        token = res.get('token')

        # 通过获取 用户信息来验证 Token
        response = self.client.post(
            '/wwwapi/v1/GetUser',
            headers=self.get_api_headers(auth_type='token', token=token)
        )
        self.assertTrue(response.status_code == 200)
        res = json.loads(response.data)

        self.assertNotIn('code', res.keys())
        self.assertIn('User', res.keys())
