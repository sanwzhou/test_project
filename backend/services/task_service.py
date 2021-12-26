# -*-coding:utf-8 -*-
# @Time  : 2021/12/26 0026 20:56
# @File  :task_service.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe: 测试任务服务

from flask import request
from flask_restful import Resource

from backend.models.task_model import Task
from backend.server import db


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
