# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : demo.py
@desc: 
@Created on: 2021/1/6 14:53
"""
import unittest
from Base.BaseSettings import StaticDIR
from Base.Beautifullib import DIYBeautifulReport
from TestCase import TestFind, TestFinds

suite=unittest.TestSuite()
TestCases = unittest.TestLoader().loadTestsFromModule(TestFind)
TestCases1 = unittest.TestLoader().loadTestsFromModule(TestFinds)


suite.addTests([TestCases,TestCases1])


# runner=unittest.TextTestRunner()
runner = DIYBeautifulReport(suite)
runner.report("测试报告","report.html",report_dir=StaticDIR)
