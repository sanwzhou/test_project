# -*-coding:utf-8 -*-
# @Time  : 2021/12/26 0026 21:06
# @File  :execution_service.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe: 执行任务服务

import json

from flask import request
from flask_restful import Resource
from jenkinsapi.jenkins import Jenkins

from backend.models.task_model import Task
from utils.handle_yaml import handle_yaml


class ExecutionService(Resource):
    """执行任务服务"""

    def __init__(self):
        self.config = handle_yaml.get_value('backend/config2.yaml', 'jenkins')
        self.host, self.port, user, token = self.config['host'], self.config['port'], self.config['user'], self.config[
            'token']
        self.jenkins = Jenkins(f'http://{self.host}:{self.port}', username=user, password=token)
        self.jenkins_job = self.jenkins[self.config['job']]

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
            # todo: jenkins任务配置allure
            # build_num = self.jenkins_job.get_last_build()
            # while True:
            #     last_build_num = self.jenkins_job.get_last_build()
            #     if last_build_num != build_num:
            #         allure_report = f'http://{self.host}:{self.port}/job/{self.config["job"]}/{last_build_num}/allure'
            #         return {'msg': 'success', 'code': '000000', 'allure_report': allure_report}
            #     else:
            #         # todo: 超时判断
            #         pass
            return {'msg': 'success', 'code': '000000'}
        else:
            return {'msg': '未找到该任务id', 'code': '100003'}
