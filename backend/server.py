# -*-coding:utf-8 -*-
# @Time  : 2021/9/23 0023 22:40
# @File  :test_testcase_server.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe: server

from flask import Flask
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from backend.settings2 import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
api = Api(app)
db = SQLAlchemy(app)
CORS(app)
auth = HTTPBasicAuth()


def router_manage():
    from backend.services.testcase_service import TestCaseService
    from backend.services.task_service import TaskService
    from backend.services.execution_service import ExecutionService
    from backend.services.login_service import LoginService, LogoutService
    from backend.services.report_service import ReportService
    from backend.services.result_service import ResultService

    api.add_resource(TestCaseService, '/testcase')
    api.add_resource(TaskService, '/task')
    api.add_resource(ExecutionService, '/execution')
    api.add_resource(ResultService, '/result')
    api.add_resource(ReportService, '/report')
    api.add_resource(LoginService, '/login')
    api.add_resource(LogoutService, '/logout')


if __name__ == '__main__':
    router_manage()
    app.run(debug=True)
