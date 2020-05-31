import unittest
from library.ddt import ddt,data
from common.readexcel import ReadExcel
import os
import jsonpath
import decimal
from common.contants import DATA_DIR
from common.myconfig import conf
from common.handle_data import replace_data,TestData
from common.handle_request import HandleRequest
from common.mylogger import my_log
from common.handle_db import HandleDB

data_file_path = os.path.join(DATA_DIR,"apicases2.xlsx")
@ddt
class TestWithdraw(unittest.TestCase):
    excel = ReadExcel(data_file_path,"withdraw")
    cases = excel.read_data()
    http = HandleRequest()
    db = HandleDB()

    @data(*cases)
    def test_withdraw(self,case):
    # 第一步：准备测试用例数据
        url = conf.get_str("env","url") + case["url"]
        data = eval(replace_data(case["data"]))
        method = case["method"]
        headers = eval(conf.get_str("env","headers"))
        if case["interface"] != "login":
            headers["Authorization"] = getattr(TestData,"token_data")

        expected = eval(case["expected"])
        row = case["case_id"]+1
        if case["check_sql"]:
            sql = replace_data(case["check_sql"])
            start_money = self.db.get_one(sql)[0]

        res = self.http.send(url=url,method=method,json=data,headers=headers)
        result = res.json()
        if case["interface"] == "login":
            id = jsonpath.jsonpath(result,"$..id")[0]
            setattr(TestData,"member_id",str(id))
            token_type = jsonpath.jsonpath(result,"$..token_type")[0]
            token = jsonpath.jsonpath(result,"$..token")[0]
            token_data = token_type + " " + token
            setattr(TestData,"token",token)

        try:
            self.assertEqual(expected["code"],result["code"])
            self.assertEqual(expected["msg"],result["msg"])
            if case["check_sql"]:
                sql = replace_data(case["check_sql"])
                end_money = self.db.get_one(sql)[0]
                withdraw_money = decimal.Decimal(str(data["amount"]))
                my_log.info("取现之前金额为:{}\n取现金额为:{}\n取现之后金额为:{}".format(start_money,withdraw_money,end_money))
                self.assertEqual(withdraw_money,start_money-end_money)


        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="未通过")
            my_log.info("用例:{}---->执行未通过".format(case["title"]))
            print("预期结果:{}".format(expected))
            print("实际结果:{}".format(result))
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")
            my_log.info("用例:{}---->执行未通过".format(case["title"]))


