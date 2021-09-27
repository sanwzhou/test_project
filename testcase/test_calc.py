# -*-conding:utf-8 -*-
# @Time  : 2021/8/22 0022 22:13
# @File  :test_calc.py
# @Author:swzhou
# @email :zhou_sanwang@163.com
# @describe: demo测试用例

import logging

# import allure
import pytest


# @allure.feature('计算器测试模块')
class Testcalc:

    # @allure.story('测试加法-整数')
    @pytest.mark.run(order=-1)
    @pytest.mark.parametrize('x,y,expected',
                             [(1, 1, 2), (1, 9, 10), (1, 0, 1)],
                             ids=['Single digit', 'Tens', 'zero'])
    def test_add_int(self, x, y, expected):
        logging.info(f'测试加法-整数功能 参数：{x, y},预期结果：{expected}')
        assert x + y == expected
