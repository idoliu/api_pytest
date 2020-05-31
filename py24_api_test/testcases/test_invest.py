import unittest
from library.ddt import ddt,data
from common.readexcel import ReadExcel
import os
import jsonpath
from common.contants import DATA_DIR
from common.myconfig import conf
from common.handle_data import TestData,replace_data
from common.handle_request import HandleRequest
from common.mylogger import my_log

data_file_path = os.path.join(DATA_DIR,"apicases2.xlsx")

@ddt
class TestInvest(unittest.TestCase):
    excel = ReadExcel(data_file_path,"invest")
    cases = excel.read_data()
    http = HandleRequest()
    @data(*cases)
    def test_invest(self,case):
        url = conf.get_str("env","url") + case["url"]
        data = eval(replace_data(case["data"]))
        method = case["method"]
        headers = eval(conf.get_str("env","headers"))
        if case["interface"] != "login":
            headers["Authorization"] = getattr(TestData, "token_data")
        expected = eval(case["expected"])
        row = case["case_id"]+1

        res = self.http.send(url=url,method=method,json=data,headers=headers)
        result = res.json()
        if case["interface"] == "login":
            token_type = jsonpath.jsonpath(result, "$..token_type")[0]
            token = jsonpath.jsonpath(result, "$..token")[0]
            token_data = token_type + " " + token
            setattr(TestData, "token_data", token_data)
            id = jsonpath.jsonpath(result, "$..id")[0]
            setattr(TestData, "member_id", str(id))

        elif case["interface"] == "add":
            loan_id = jsonpath.jsonpath(result,"$..id")[0]
            setattr(TestData,"loan_id",str(loan_id))

        try:
            self.assertEqual(expected["code"], result["code"])
            self.assertEqual(expected["msg"], result["msg"])
        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="未通过")
            my_log.info("用例:{}---->执行未通过".format(case["title"]))
            print("预期结果:{}".format(expected))
            print("实际结果:{}".format(result))
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")
            my_log.info("用例:{}---->执行未通过".format(case["title"]))
