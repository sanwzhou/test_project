# -*- coding: utf-8 -*-
# @Time : 2021/9/27 15:36
# @Author : swzhou
# @FileName: handle_yaml.py
# @Email   : zhou_sanwang@163.com
# @Software: PyCharm
# @describe: 操作yaml

import yaml
from utils.get_config import project_dir


class HandleYaml:

    @staticmethod
    def load_yaml(file):
        file_path = project_dir / file
        with open(file_path, encoding='utf8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def get_value(self, file, key1=None, key2=None):
        data = self.load_yaml(file)
        if key1:
            data = data.get(key1, None)
            if key2:
                data = data.get(key2, None)
        return data


handle_yaml = HandleYaml()

if __name__ == '__main__':
    file = 'backend/config2.yaml'
    # print(handle_yaml.get_value(file))
    # print(handle_yaml.get_value(file, 'jenkins'))
