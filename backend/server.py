from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['db'] = []

ip = 'x.x.x.x'
db_user = 'xxx'
db_passwd = 'xxxx'
db_name = 'flask_test_project'

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_passwd}@{ip}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    passwd = db.Column(db.String(16))

    def __repr__(self):
        return jsonify(id=self.id, name=self.name)


class TestCase(db.Model):
    __tablename__ = 'testcases'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    steps = db.Column(db.String(1024), nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return jsonify(id=self.id, name=self.name, )


class TestCaseService(Resource):
    """
    测试用例服务
    状态码：
        {'msg': 'success', 'code': '000000'}
        {'msg': '添加用例失败', 'code': '100001'}
        {'msg': '删除用例失败', 'code': '100002'}
        {'msg': '未找到该用例id', 'code': '100003'}
    """

    def get(self):
        """查询用例"""
        case_id = request.args.get('case_id', None)
        name = request.args.get('case_id', None)

        if case_id:
            cases = TestCase.query.get(case_id)
        elif name:
            cases = TestCase.query.filter_by(name=name).first()
        else:
            cases = TestCase.query.all()

        case_list = [{'id': case.id, 'name': case.name, 'steps': case.steps, 'description': case.description} for case
                     in cases]

        return {'msg': 'success', 'code': '000000', 'testcase': case_list}

    def post(self, name, steps, description=None):
        """新增测试用例"""
        # todo:修改传参
        try:
            case = TestCase(name=name, steps=steps, description=description)
            db.session.add(case)
            db.session.commit()
        except Exception as e:
            print('添加失败')
            print(e)
            db.session.callback()
            return {'msg': '添加用例失败', 'code': '100001'}

        return {'msg': 'success', 'code': '000000'}

    def delete(self, case_id):
        """todo:删除测试用例"""
        # todo:修改传参
        case = TestCase.query.get(case_id)
        if case:
            try:
                case.delete()
            except Exception as e:
                print('删除失败')
                print(e)
                db.session.callback()
                return {'msg': '删除用例失败', 'code': '100002'}
        else:
            print(f'未找到该用例id:{case_id}')
            return {'msg': '未找到该用例id', 'code': '100003'}
        return {'msg': 'success', 'code': '0'}


api.add_resource(TestCaseService, '/testcase')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
