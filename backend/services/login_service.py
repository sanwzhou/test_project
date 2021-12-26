# -*-coding:utf-8 -*-
# @Time  : 2021/12/26 0026 21:09
# @File  :login_service.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe: 登录登出服务

from flask import request, url_for
from flask_restful import Resource

from backend.auth import user_token
from backend.models.user_model import User
from backend.server import app


class LoginService(Resource):
    """登录"""

    @staticmethod
    def post():
        username = request.json.get('username')
        password = request.json.get('password')
        if username and password:
            user = User.query.filter_by(name=username).first()
            if not user:
                return {'msg': '账号不存在', 'code': '200003'}
            elif user.passwd != password:
                return {'msg': '账号/密码不匹配', 'code': '200004'}
        else:
            return {'msg': '账号/密码不能为空', 'code': '200002'}

        token = user_token.generate_auth_token(user.id).decode(encoding='utf-8')
        return {'msg': 'login success', 'code': '000000', 'token': token}


class LogoutService(Resource):
    """退出"""

    @staticmethod
    def post():
        # username = request.json.get('username')
        # if username:
        #     pass
        return {'msg': 'logout success', 'code': '000000'}


@app.before_request
def is_login():
    # g.user = None
    if request.path != url_for('loginservice'):  # "/login"
        status = user_token.verify_passwd(request.headers.get('token', None))
        if not status:
            return {'msg': 'token验证失败,请登录后访问', 'code': '200001'}
