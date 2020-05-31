import unittest
from library.HTMLTestRunnerNew import HTMLTestRunner
from common.contants import CASE_DIR,REPORT_DIR
import os

suite = unittest.TestSuite()

loader = unittest.TestLoader()
suite.addTest(loader.discover(CASE_DIR))

report_path = os.path.join(REPORT_DIR,'report.html')
with open(report_path,"wb") as f:
    runner = HTMLTestRunner(stream=f,
                   title="24期的测试报告",
                   description="验证相注册登录功能",
                   tester="musen")

    runner.run(suite)