# -*-coding:utf-8 -*-
# @Time  : 2021/12/26 0026 20:54
# @File  :task_model.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe: 测试任务表结构

import json

from backend.models.testcase_model import TestCase
from backend.server import db


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
