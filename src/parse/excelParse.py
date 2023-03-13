import os,sys
sys.path.append(os.getcwd())
import xlrd

class ExcelRead():
    def __init__(self, filename = "", sheet_name = "Sheet1"):
        self.__workbook = xlrd.open_workbook(filename)
        self.__sheet = self.__workbook.sheet_by_name(sheet_name)

    def get_workbook(self):
        return self.__workbook

    def get_sheet(self):
        return self.__sheet

    def get_ncols(self):
        return self.__sheet.ncols

    def get_nrows(self):
        return self.__sheet.nrows

    def readline(self, line_num = 0):
        line = []
        for _ in range(self.__sheet.ncols):
            line.append(self.__sheet.cell_value(line_num, _))
        return line

    def readAll(self):
        lines = []
        for row in range(self.__sheet.nrows):
           lines = lines + self.readline(row)
        return lines


#from config import Config_Parser
#if __name__ == '__main__':
#    print(Config_Parser("testfile/test_config.ini").get_config('Test_Report', 'txt_title'))

if __name__ == '__main__':
     test = ExcelRead("testfile/test.xls")
     print(test.readAll())