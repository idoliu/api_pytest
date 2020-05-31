import openpyxl
class CaseData:
    pass
class ReadExcel():
    def __init__(self,filename,sheetname):
        self.filename = filename
        self.sheetname = sheetname
    def open(self):
        self.workbook = openpyxl.load_workbook(self.filename)
        self.sheet = self.workbook[self.sheetname]
    def read_data(self):
        self.open()
        rows = list(self.sheet.rows)
        title = []
        for r in rows[0]:
            title.append(r.value)
        cases = []
        for row in rows[1:]:
            data = []
            for r in row:
                data.append(r.value)
            case = dict(zip(title, data))
            cases.append(case)
        self.workbook.close()
        return cases

    def read_data_obj(self):
        self.open()
        row = list(self.sheet.rows)
        title = []
        for r in rows[0]:
            title.append(r.value)
        cases = []
        for row in rows[1:]:
            data = []
            for r in row:
                data.append(r.value)
            case = list(zip(title, data))
            case_obj = CaseData()
            for k,v in case:
                setattr(case_obj,k,v)

            cases.append(case_obj)
        return cases
    def write_data(self,row,column,value):
        self.open()
        self.sheet.cell(row=row,column=column,value=value)
        self.workbook.save(self.filename)


if __name__ == '__main__':
    ReadExcel("cases.xlsx","register")
    data = excel.read_data_obj()
    print(data)

