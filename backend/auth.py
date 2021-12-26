# -*-coding:utf-8 -*-
# @Time  : 2021/10/29 0029 10:09
# @File  :auth.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe: token
import re

from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from backend.models.user_model import User
from utils.handle_yaml import handle_yaml


class UserToken:
    auth = HTTPBasicAuth()
    SECRET_KEY = handle_yaml.get_value('backend/config2.yaml', 'login', 'secret_key')

    def generate_auth_token(self, user_id, expiration=3600):
        s = Serializer(self.SECRET_KEY, expires_in=expiration)
        return s.dumps({'user_id': user_id})

    def verify_auth_token(self, token):
        """验证 登录token"""
        s = Serializer(self.SECRET_KEY)
        if isinstance(token, str):
            token = token.encode('utf-8')
        elif isinstance(token, bytes):
            pass
        else:
            raise Exception('token类型非str、非bytes')

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        user = User.query.filter_by(id=data['user_id']).first()
        # print('user:',user)
        return user

    @staticmethod
    @auth.verify_password
    def verify_passwd(username_or_token, password=None):
        """验证token 、 验证账号密码"""
        username_or_token = re.sub(r'^"|"$', '', str(username_or_token))
        user = user_token.verify_auth_token(username_or_token)
        if not user:
            from backend.server import User
            user = User.query.filter_by(name=username_or_token).first()
            if not user or user.passwd != password:
                return False
        return True


user_token = UserToken()

if __name__ == '__main__':
    token = user_token.generate_auth_token('1').decode('utf-8')
    print(token)
    data = user_token.verify_auth_token(token)
    print(data)
    # data = user_token.verify_auth_token('123')
    # print(data)
    # data = user_token.verify_passwd('1')
    # print(data)
    # data = user_token.verify_passwd('sw')
    # print(data)
