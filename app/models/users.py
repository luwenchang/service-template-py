# -*- coding: utf-8 -*-
__author__ = 'vincent'

from .common import *
from datetime import datetime
import uuid


class User(db.Model, TableBase):
    __tablename__ = 'users'

    id = db.Column(db.String(65), index=True, unique=True)
    nickname = db.Column(db.String(128), index=True, unique=True, comment='昵称')
    email = db.Column(db.String(128), index=True, unique=True, comment='邮件地址')
    mobile = db.Column(db.String(32), index=True, unique=True, comment='移动电话')
    note = db.Column(db.Text, comment='备注信息')
    name = db.Column(db.String(128), comment='姓名')
    intro = db.Column(db.Text, comment='个人简介')
    head_portrait = db.Column(db.Text, comment='用户头像地址')
    is_disabled = db.Column(TINYINT(display_width=1), nullable=False, default=0, comment='帐号是否被禁用')


    #
    # # 用户AK关联 相关
    # aks = db.relationship('UserAK', backref='user', lazy='dynamic')
    #

    # 用户本地用户密码登录 相关
    local_login = db.relationship('UserLocalAuth', backref='user', cascade='delete, delete-orphan', lazy='dynamic')

    #
    # # 用户登录历史记录
    # login_history_list = db.relationship('LoginHistory', backref='user', lazy='dynamic')
    #

    _to_dict_default_fields_ = ['id', 'nickname', 'email', 'mobile', 'note', 'name', 'intro', 'head_portrait',
                                'is_disabled']

    def __repr__(self):
        return '<id %r, nickname %s, email %s, mobile %s>' % (self.id, self.nickname, self.email, self.mobile)



class UserLocalAuth(db.Model, TableBase):
    __tablename__ = 'userLocalAuth'

    user_id = db.Column(db.ForeignKey('users.id'), index=True, primary_key=True)
    xname = db.Column(db.String(65), nullable=False, unique=True, comment='系统自定分配的用户名盐')
    password_hash = db.Column(db.String(65), comment='用户加密后的密码')


    def __repr__(self):
        return '<xname %r, password_hash %s, user_id %s>' % (self.xname, self.password_hash, self.user_id)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = toolkit.get_salted_password_hash(
            self.xname,
            password,
            Cfg.get('webServer', {}).get('secret'),
            Cfg.get('webServer', {}).get('str_format')
        )

    def verify_password(self, password):
        '''验证用户密码，注意这个password一定是经过md5加密的'''
        password_hash = toolkit.get_salted_password_hash(
            self.xname,
            password,
            Cfg.get('webServer', {}).get('secret'),
            Cfg.get('webServer', {}).get('str_format')
        )
        if password_hash == self.password_hash:
            return True
        else:
            return False


    def reset_password(self, new_password):
        '''重置密码'''
        self.xname = uuid.uuid4().hex
        self.password = new_password
        db.session.add(self)
        return True


    def reset_email(self, new_email):
        '''重置邮件'''
        if new_email is None:
            return False

        if self.query.filter(User.email == new_email).first() is not None:
            # 新邮件在 当前实验室的用户列表中已存在
            return False
        # 更新邮件
        self.email = new_email
        db.session.add(self)
        return True
#
#
#     def ping(self):
#         '''更新用户的最后一次访问时间'''
#         self.lastSeenTime = datetime.utcnow()
#         db.session.add(self)
#
#
# class UserAK(db.Model, TableBase):
#     __tablename__ = 'userAK'
#
#     id = db.Column(db.String(65), nullable=False, unique=True)
#     api_key = db.Column(db.String(65), nullable=False, server_default=db.FetchedValue())
#     api_secret = db.Column(db.String(65), nullable=False, server_default=db.FetchedValue())
#     is_disabled = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
#
#     users_id = db.Column(db.ForeignKey('users.id'), primary_key=True)
#



# class UserOAuth(db.Model, TableBase):
#     # 第三方登录方式暂时禁用
#     __tablename__ = 'userOAuth'
#
#     id = db.Column(db.BigInteger, nullable=False, unique=True)
#     oauth_name = db.Column(db.String(65), nullable=False, server_default=db.FetchedValue())
#     oauth_id = db.Column(db.String(65), nullable=False, unique=True, server_default=db.FetchedValue())
#     oauth_access_token = db.Column(db.String(65), nullable=False, server_default=db.FetchedValue())
#     oauth_expires = db.Column(db.String(65), nullable=False, server_default=db.FetchedValue())
#
#     users_id = db.Column(db.ForeignKey(u'users.id'), primary_key=True)

# class LoginHistory(db.Model, TableBase):
#     __tablename__ = 'userOAuth'
#
#     id = db.Column(db.BigInteger, nullable=False, unique=True, autoincrement=True)
#     oauth_name = db.Column(db.String(65), nullable=False, server_default=db.FetchedValue())
#     oauth_id = db.Column(db.String(65), nullable=False, unique=True, server_default=db.FetchedValue())
#     oauth_access_token = db.Column(db.String(65), nullable=False, server_default=db.FetchedValue())
#     oauth_expires = db.Column(db.String(65), nullable=False, server_default=db.FetchedValue())
#
#     users_id = db.Column(db.ForeignKey(u'users.id'), primary_key=True)
#
#


# class User(UserMixin, db.Model, TableBase):
#     __tablename__ = 'users'
#     __table_args__ = (
#         db.Index('email_internalUser', 'email', 'internalUserId', unique=True),
#         db.Index('internalUser_token', 'internalUserId', 'labUserSignInToken'),
#         db.Index('mobile_internalUser', 'mobile', 'internalUserId', unique=True)
#     )
#
#     id = db.Column(db.String(65), nullable=False, unique=True, server_default=db.text("''"))
#     internalUserId = db.Column(db.String(65))
#     username = db.Column(db.String(128), unique=True)
#     email = db.Column(db.String(128))
#     mobile = db.Column(db.String(32))
#     password_hash = db.Column(db.String(64))
#     note = db.Column(db.Text)
#     name = db.Column(db.String(512))
#     company = db.Column(db.String(512))
#     locale = db.Column(db.String(8), nullable=False, server_default=db.text("'zh-CN'"))
#     position = db.Column(db.String(512))
#     intro = db.Column(db.Text)
#     groupId = db.Column(db.String(65))
#     lastSignInTime = db.Column(db.DateTime)
#     lastSeenTime = db.Column(db.DateTime)
#     isLabUser = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
#     isIndependent = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
#     labUserSignInToken = db.Column(db.String(64))
#     avatarFileURL = db.Column(db.Text)
#     noBalanceQuota = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
#     labUserBalanceQuota = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
#     isDisabled = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
#     cache_labUserBalance = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
#
#     # 允许 to_dict 展示的字段列表
#     _to_dict_default_fields_=['seq', 'id', 'internalUserId', 'labUserSignInToken', 'avatarFileURL', 'username', 'email',
#                       'mobile', 'note', 'name', 'company', 'locale', 'position', 'intro', 'groupId',
#                       'lastSignInTime', 'lastSeenTime', 'isLabUser', 'isIndependent', 'noBalanceQuota',
#                       'labUserBalanceQuota', 'isDisabled', 'cache_labUserBalance',
#                       'createTimestamp', 'updateTimestamp']
#
#     @property
#     def password(self):
#         raise AttributeError('password is not a readable attribute')
#
#     @password.setter
#     def password(self, password):
#         self.password_hash = toolkit.get_salted_password_hash(
#             self.id,
#             password,
#             Cfg.get('webServer', {}).get('secret'),
#             Cfg.get('webServer', {}).get('str_format')
#         )
#
#     def verify_password(self, password):
#         '''验证用户密码，注意这个password一定是经过md5加密的'''
#         password_hash = toolkit.get_salted_password_hash(
#             self.id,
#             password,
#             Cfg.get('webServer', {}).get('secret'),
#             Cfg.get('webServer', {}).get('str_format')
#         )
#         if password_hash == self.password_hash:
#             return True
#         else:
#             return False
#
#     def generate_confirmation_token(self, expiration=3600):
#         '''生成一个用户令牌，有效期默认为1小时'''
#         s = Serializer(current_app.config['TOKEN_SECRET_KEY'], expiration)
#         return s.dumps({'confirm' : self.id, 'is_internal_user': False})
#
#     def confirm(self, token):
#         '''认证用户token'''
#         s = Serializer(current_app.config['TOKEN_SECRET_KEY'])
#         try:
#             data = s.loads(token)
#         except:
#             return False
#
#         if data.get('confirm') != self.id:
#             return False
#
#         self.confirmed = True
#         db.session.add(self)
#         return True
#
#     def reset_password(self, new_password):
#         '''重置密码'''
#         self.password = new_password
#         db.session.add(self)
#         return True
#
#     def change_email(self, new_email):
#         '''重置邮件'''
#         if new_email is None:
#             return False
#
#         if self.query.filter(and_(
#             User.internalUserId == self.internalUserId,
#             User.email == new_email)).first() is not None:
#             # 新邮件在 当前实验室的用户列表中已存在
#             return False
#         # 更新邮件
#         self.email = new_email
#         db.session.add(self)
#         return True
#
#     def is_administrator(self):
#         '''判断是否为管理员-外部站用户默认为False'''
#         return False
#
#     def ping(self):
#         '''更新用户的最后一次访问时间'''
#         self.lastSeenTime = datetime.utcnow()
#         db.session.add(self)
#
#
#
#

