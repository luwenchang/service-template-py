# -*- coding: utf-8 -*-
__author__ = 'vincent'

from flask import current_app, g
from flask import Blueprint
from flask_restful import Api

from app.utils.loggers import get_logger

logger = get_logger('api_www')

api_bp = Blueprint('api_www', __name__)

api = Api(api_bp)


from . import authentication

from .apis.token import GetToken

from .apis.user import GetUser
from .apis.user import SetUser




"""
@api {post} /GetToken 获取Token
@apiVersion 0.1.0
@apiName GetToken
@apiGroup auth

@apiHeader {String} account 帐号或token,格式 <实验室ID>/[<帐号>,<token>]:<password>

@apiParam {Number} id Users unique ID.

@apiSuccess {String} firstname Firstname of the User.
@apiSuccess {String} lastname  Lastname of the User.

@apiExample {Httpie} Httpie
    http  --json POST http://127.0.0.1:5000/wwwapi/v1/GetToken  lab_id=<lab_id> account=<account>  password=<password_md5>

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
      "expiration": 3600,
      "token": "xxxxxxxxxxxxxxx"
    }

@apiError UserNotFound The <code>id</code> of the User was not found.

@apiErrorExample Error-Response:
    HTTP/1.1 500 Not Found
    {
        "message": "Internal Server Error"
    }
 """
api.add_resource(GetToken, '/GetToken')



api.add_resource(GetUser, '/GetUser')



api.add_resource(SetUser, '/SetUser')




