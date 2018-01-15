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


from datetime import datetime
import uuid


class APITestCase(unittest.TestCase):

    def setUp(self):
        '''
        该方法创建一个测试环境，类似与运行中的环境
        '''
        # 使用测试配置创建一个程序
        self.app = create_app('TestConfig')
        # 激活上下文
        self.app_context = self.app.app_context()
        # 推送程序上下文
        self.app_context.push()
        # 创建一个全新的数据库
        db.create_all()
        # Role.insert_roles()
        # 创建Flask测试客户端对象，在该对象上可调用方法向程序发起请求。
        # 如果测试客户端启用了 use_cookies 选项，那么这个客户端就能像浏览器一样接收和发送 cookie,因此能够使用依赖cookie的功能记住请求之间的上下文
        # self.client = self.app.test_client(use_cookies=True)
        # 因 API 的测试无需浏览器支持，所以此处可以去掉 参数 use_cookies
        self.client = self.app.test_client()

    def tearDown(self):
        '''
        这是测试完成之后会自动运行的方法，本方法将删除 程序上下文和数据库
        '''
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, auth_type, account=None, password=None, token=None):
        '''获取 api header'''

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Auth-Type' : auth_type
        }

        if account and password:
            headers['Authorization'] = 'Basic ' + b64encode(
                (account + ':' + password).encode('utf-8') ).decode('utf-8')

        if token:
            headers['Authorization'] = token

        return headers


    def add_users(self, count=100):
        '''该方法用于生成大批量的虚拟信息'''
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py
        import random
        result = []

        seed()
        for i in range(count):
            username = forgery_py.name.full_name()
            user_id = uuid.uuid4().hex
            mobile = int(random.random() * 100000000)
            email = forgery_py.internet.email_address()

            u = User(id=user_id, nickname=username, email=email, mobile=mobile, name=username, is_disabled=0)

            ul = UserLocalAuth(user_id=u.id, xname=uuid.uuid4().hex, password=get_password_md5(username))


            db.session.add_all([u, ul])

            try:
                db.session.commit()
                result.append(user_id)
            except IntegrityError:
                db.session.rollback()

        return result


    def test_add_user(self):
        '''验证批量添加用户是否成功'''
        count = 10
        u = User.query.all()
        c1 = len(u)
        self.add_users(count)

        u2 = User.query.all()
        self.assertTrue(c1+count ==len(u2))

    def test_check_user_password(self):
        '''验证用户的密码'''
        self.add_users(10)
        user_list = User.query.all()
        u1 = user_list[0]

        u1_login_info = u1.local_login.first()
        self.assertTrue(u1_login_info.verify_password(get_password_md5(u1.nickname)))
        self.assertFalse(u1_login_info.verify_password(get_password_md5('121212')))


    def test_user_reset_password(self):
        '''验证重置密码'''
        user_id_list = self.add_users(1)
        u = User.query.filter_by(id=user_id_list[0]).first()

        login_info = u.local_login.first()

        self.assertTrue(login_info.verify_password(get_password_md5(u.nickname)))

        login_info.reset_password(get_password_md5('12ABC'))
        db.session.add(login_info)
        self.assertTrue(login_info.verify_password(get_password_md5('12ABC')))
        self.assertFalse(login_info.verify_password(get_password_md5(u.nickname)))


    def test_api_GetToken(self):
        '''验证-api-获取Token'''
        user_id_list = self.add_users(1)
        u = User.query.filter_by(id=user_id_list[0]).first()


        # 验证密码错误的请求
        response = self.client.post(
            url_for('api_www.gettoken'),
            headers=self.get_api_headers(auth_type='email-password'  , account=u.email, password=get_password_md5(u.nickname))
        )
        self.assertTrue(response.status_code == 200)
