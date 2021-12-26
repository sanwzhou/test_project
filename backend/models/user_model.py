# -*-coding:utf-8 -*-
# @Time  : 2021/12/26 0026 21:05
# @File  :user_model.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe: 用户表结构

from backend.server import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    passwd = db.Column(db.String(16))

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'