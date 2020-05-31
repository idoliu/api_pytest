import unittest
import os
import random
from common.readexcel import ReadExcel
from common.contants import DATA_DIR
from library.ddt import ddt,data
from common.myconfig import conf
from common.handle_request import HandleRequest
from common.mylogger import my_log
import jsonpath
from common.handle_db import HandleDB

data_file_path = os.path.join(DATA_DIR,"apicases2.xlsx")

@ddt
class TestRecharge(unittest.TestCase):
    excel = ReadExcel(data_file_path,"recharge")
    cases = excel.read_data()
    http = HandleRequest()
    db = HandleDB()

    @classmethod
    def setUpClass(cls):
         # 登录，获取用户id和鉴权需要用到的token
        url = conf.get_str("env", "url") + "/member/login"
        data = {
            "mobile_phone":conf.get_str("test_data","user"),
            "pwd":conf.get_str("test_data","pwd")
        }
        headers = eval(conf.get_str("env","headers"))
        response = cls.http.send(url=url,method="post",json=data,headers=headers)
        json_data = response.json()
        #  登录之后从响应结果中提取用户id和token
        # 提取用户id
        cls.member_id = jsonpath.jsonpath(json_data,"$..id")[0]
        # 提取token
        token_type = jsonpath.jsonpath(json_data,"$..token_type")[0]
        token = jsonpath.jsonpath(json_data,"$..token")[0]
        cls.token_data = token_type + " " + token
        cls.leave_amount = jsonpath.jsonpath(json_data,"$..leave_amount")[0]


    @data(*cases)
    def test_recharge(self,case):
        # 第一步：准备测试用例数据
        # 拼接完整的接口地址
        url = conf.get_str("env", "url") + case["url"]
        # 请求方法
        method = case["method"]
        # 请求参数
        # 判断是否有用户id需要替换
        if "#member_id#" in case["data"]:
            case["data"] = case["data"].replace("#member_id#",str(self.member_id))

        data = eval(case["data"])
        # 请求头
        headers = eval(conf.get_str("env", "headers"))
        headers["Authorization"] = self.token_data
        # 预期结果
        expected = eval(case["expected"])
        # 该用例在该表单中所在行
        row = case["case_id"] + 1

        # 第二步：发送请求到接口，获取实际结果
        response = self.http.send(url=url, method=method, json=data, headers=headers)
        result = response.json()

        # 第三步：比对预期结果和实际结果
        try:
            self.assertEqual(expected["code"], result["code"])
            self.assertEqual(expected["msg"], result["msg"])
            if result["msg"] == "OK":

                sql = "select leave_amount from futureloan.member where id={}".format(self.member_id)
                # 获取数据库中有没有该用户的信息
                data = self.db.get_one(sql)
                print(data)


                # self.assertEqual(1, count)
        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="未通过")
            my_log.info("用例:{}---->执行未通过".format(case["title"]))
            print("预期结果:{}".format(expected))
            print("实际结果:{}".format(result))
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")
            my_log.info("用例:{}---->执行未通过".format(case["title"]))



