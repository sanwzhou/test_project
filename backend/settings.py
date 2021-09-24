# -*- coding: utf-8 -*-
# @Time : 2021/9/24 14:05
# @Author : swzhou
# @FileName: settings.py
# @Email   : zhou_sanwang@163.com
# @describe: flask app配置文件

class BaseConfig:
    debug = True
    port = 5000

    db_ip = 'x.x.x.x'
    db_port = 3306
    db_user = 'xxx'
    db_passwd = 'xxx'
    db_name = 'flask_test_project'

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_passwd}@{db_ip}:{db_port}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
