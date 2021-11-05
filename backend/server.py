# -*-coding:utf-8 -*-
# @Time  : 2021/9/23 0023 22:40
# @File  :test_testcase_server.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe: server

import json

from flask import Flask, request, url_for
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from jenkinsapi.jenkins import Jenkins

from backend.auth import user_token
from backend.settings2 import BaseConfig
from utils.handle_yaml import handle_yaml

app = Flask(__name__)
app.config.from_object(BaseConfig)
api = Api(app)
db = SQLAlchemy(app)
CORS(app)
auth = HTTPBasicAuth()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    passwd = db.Column(db.String(16))

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'


class TestCase(db.Model):
    """测试用例表"""
    __tablename__ = 'testcases'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    steps = db.Column(db.String(1024), nullable=True)
    description = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return f'<id: {self.id}, name: {self.name}>'

    def as_dict(self):
        return {'id': self.id, 'name': self.name, 'steps': self.steps, 'description': self.description}


class Task(db.Model):
    """测试任务表"""
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True, nullable=False)
    testcases = db.Column(db.String(1024), nullable=False)
    description = db.Column(db.String(1024), nullable=True)

    def __repr__(self):
        return f'<task_id: {self.id}, name: {self.name}>'

    def as_dict(self):
        testcase_ids = json.loads(self.testcases)
        case_names = []
        for case_id in testcase_ids:
            testcase = TestCase.query.filter_by(id=case_id).first()
            case_names.append(testcase.name)

        return {"id": self.id, 'name': self.name, 'testcases': json.loads(self.testcases),
                "command": "pytest.main(['" + "','".join(case_names) + "'])"}


class Result(db.Model):
    """测试结果"""
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    testcase_id = db.Column(db.Integer, db.ForeignKey('testcases.id'))
    status = db.Column(db.String(120), nullable=True)
    outpot = db.Column(db.String(1024), nullable=True)

    def as_dict(self):
        return {'id': self.id, 'testcase_id': self.testcase_id, 'status': self.status, 'outpot': self.outpot}


class TestCaseService(Resource):
    """
    测试用例服务
    状态码：
        {'msg': 'success', 'code': '000000'}
        {'msg': '添加用例失败', 'code': '100001'}
        {'msg': '删除用例失败', 'code': '100002'}
        {'msg': '未找到该用例id', 'code': '100003'}
    """

    @staticmethod
    def get():
        """查询用例"""
        case_id = request.args.get('case_id', None)
        name = request.args.get('name', None)

        if case_id:
            cases = TestCase.query.filter_by(id=case_id)
        elif name:
            cases = TestCase.query.filter_by(name=name)
        else:
            cases = TestCase.query.all()

        return {'msg': 'success', 'code': '000000', 'testcase': [case.as_dict() for case in cases]}

    @staticmethod
    def post():
        """新增测试用例"""
        name = request.json.get('name')
        steps = request.json.get('steps')
        description = request.json.get('description')

        try:
            case = TestCase(name=name, steps=steps, description=description)
            db.session.add(case)
            db.session.commit()
        except Exception as e:
            print('添加失败')
            print(e)
            db.session.rollback()
            return {'msg': '用例添加失败', 'code': '100001'}
        return {'msg': 'success', 'code': '000000'}

    @staticmethod
    def put():
        """修改测试用例"""
        case_id = request.json.get('id')

        if case_id and TestCase.query.get(case_id):
            name = request.json.get('name')
            steps = request.json.get('steps')
            description = request.json.get('description')

            try:
                case = TestCase.query.filter_by(id=case_id).first()
                case.name = name
                case.steps = steps
                case.description = description
                db.session.add(case)
                db.session.commit()
            except Exception as e:
                print('修改失败')
                print(e)
                db.session.rollback()
                return {'msg': '用例修改失败', 'code': '100001'}
            return {'msg': 'success', 'code': '000000'}
        else:
            return {'msg': '未找到该用例id', 'code': '100003'}

    @staticmethod
    def delete():
        """删除指定测试用例"""
        case_id = request.json.get('case_id')

        case = TestCase.query.get(case_id)
        if case:
            try:
                TestCase.query.filter_by(id=case_id).delete()
                db.session.commit()
            except Exception as e:
                print('删除失败')
                print(e)
                db.session.rollback()
                return {'msg': '用例删除失败', 'code': '100002'}
        else:
            print(f'未找到该用例id:{case_id}')
            return {'msg': '未找到该用例id', 'code': '100003'}
        return {'msg': 'success', 'code': '000000'}


class TaskService(Resource):
    """
    测试任务服务
        {'msg': 'success', 'code': '000000'}
        {'msg': '添加任务失败', 'code': '100001'}
        {'msg': '删除任务失败', 'code': '100002'}
        {'msg': '未找到该任务id', 'code': '100003'}
    """

    @staticmethod
    def get():
        task_id = request.args.get('task_id')
        task_name = request.args.get('task_name')

        if task_id:
            tasks = Task.query.filter_by(id='task_id')
        elif task_name:
            tasks = Task.query.filter_by(name='task_name')
        else:
            tasks = Task.query.all()

        return {'msg': 'success', 'code': '000000', 'tasks': [task.as_dict() for task in tasks]}

    @staticmethod
    def post():
        name = request.json.get('name')
        description = request.json.get('description')
        testcases = request.json.get('testcases')

        try:
            task = Task(name=name, description=description, testcases=testcases)
            db.session.add(task)
            db.session.commit()
        except Exception as e:
            print('添加任务失败')
            print(e)
            db.session.rollback()
            return {'msg': '添加任务失败', 'code': '100001'}
        return {'msg': 'success', 'code': '000000'}

    @staticmethod
    def delete():
        task_id = request.json.get('task_id')
        task = Task.query.get(task_id)
        if task:
            try:
                Task.query.filter_by(id=task_id).delete()
                db.session.commit()
            except Exception as e:
                print('删除任务失败')
                print(e)
                db.session.rollback()
                return {'msg': '删除任务失败', 'code': '100002'}
        else:
            return {'msg': '未找到该任务id', 'code': '100003'}
        return {'msg': 'success', 'code': '000000'}


class ExecutionService(Resource):
    """执行任务服务"""

    def __init__(self):
        config = handle_yaml.get_value('backend/config2.yaml', 'jenkins')
        host, port, user, token = config['host'], config['port'], config['user'], config['token']
        self.jenkins = Jenkins(f'http://{host}:{port}', username=user, password=token)
        self.jenkins_job = self.jenkins[config['job']]

    def get(self):
        # res = self.jenkins.version
        # print(res)
        pass

    def post(self):
        task_id = request.json.get('task_id')
        if task_id:
            task = Task.query.filter_by(id=task_id).first()
            self.jenkins_job.invoke(build_params={
                'task': json.dumps(task.as_dict()),
                'task_id': task.id,
                'command': task.as_dict()['command']
            })
            return {'msg': 'success', 'code': '000000'}
        else:
            return {'msg': '未找到该任务id', 'code': '100003'}


class ResultService(Resource):
    """测试结果保存"""

    @staticmethod
    def get():
        testcase_id = request.args.get('testcase_id')
        if testcase_id:
            results = Result.query.filter_by(testcase_id=testcase_id)
        else:
            results = Result.query.all()

        return {'msg': 'success', 'code': '000000', 'results': [r.as_dict() for r in results]}

    @staticmethod
    def post():
        testcase_id = request.json.get('testcase_id')
        status = request.json.get('status')
        outpot = request.json.get('outpot')
        try:
            result = Result(testcase_id=testcase_id, status=status, outpot=outpot)
            db.session.add(result)
            db.session.commit()
        except Exception as e:
            print('保存用例执行结果失败')
            print(e)
            db.session.rollback()
            return {'msg': '保存用例执行结果失败', 'code': '100001'}
        return {'msg': 'success', 'code': '000000'}


class ReportService(Resource):
    """查询测试结果生成测试报告"""

    @staticmethod
    def get():
        pass

    @staticmethod
    def post():
        pass


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


api.add_resource(TestCaseService, '/testcase')
api.add_resource(TaskService, '/task')
api.add_resource(ExecutionService, '/execution')
api.add_resource(ResultService, '/result')
api.add_resource(ReportService, '/report')
api.add_resource(LoginService, '/login')
api.add_resource(LogoutService, '/logout')


if __name__ == '__main__':
    app.run(debug=True)
