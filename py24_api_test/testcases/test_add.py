import unittest
from library.ddt import ddt,data
from common.readexcel import ReadExcel
import os
from common.contants import DATA_DIR
from common.myconfig import conf
from common.handle_data import replace_data,TestData
from common.handle_request import HandleRequest
import jsonpath
from common.mylogger import my_log
from common.handle_db import HandleDB

file_path = os.path.join(DATA_DIR,"apicases2.xlsx")


@ddt
class TestAdd(unittest.TestCase):
    excel = ReadExcel(file_path,"add")
    cases = excel.read_data()
    http = HandleRequest()
    db = HandleDB()
    @data(*cases)
    def test_add(self,case):
        # 第一步：准备用例数据
        url = conf.get_str("env","url") + case["url"]
        case["data"] = replace_data(case["data"])
        data = eval(case["data"])
        headers = eval(conf.get_str("env","headers"))
        if case["interface"] != "login":
            headers["Authorization"] = getattr(TestData,"token_data")
        expected = eval(case["expected"])
        method = case["method"]
        row = case["case_id"] + 1
        # 第二步：发送请求
        if case["check_sql"]:
            sql = replace_data(case["check_sql"])
            s_loan_num = self.db.count(sql)
        res = self.http.send(url=url,method=method,json=data,headers=headers)
        result = res.json()
        if case["interface"] == "login":
            token_type = jsonpath.jsonpath(result,"$..token_type")[0]
            token = jsonpath.jsonpath(result, "$..token")[0]
            token_data = token_type + " " + token
            setattr(TestData,"token_data",token_data)
            id = jsonpath.jsonpath(result,"$..id")[0]
            setattr(TestData,"admin_member_id",str(id))
        # 第三步：比对结果（断言）
        try:
            self.assertEqual(expected["code"],result["code"])
            self.assertEqual(expected["msg"],result["msg"])
            if case["check_sql"]:
                sql = replace_data(case["check_sql"])
                end_loan_num = self.db.count(sql)
                self.assertEqual(end_loan_num - s_loan_num,1)


        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="未通过")
            my_log.info("用例:{}---->执行未通过".format(case["title"]))
            print("预期结果:{}".format(expected))
            print("实际结果:{}".format(result))
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")
            my_log.info("用例:{}---->执行未通过".format(case["title"]))








