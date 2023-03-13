import unittest
import os,sys
sys.path.append(os.getcwd())
from diag import Diag
import time
from TestStart import label
from parse import Config_Parser
from parse.excelParse import ExcelRead
from logger import Logger
log = Logger()

@label(module = "diag")
class Diag_Test(unittest.TestCase):

    @label(priority="P1")
    def test_0_sa(self):
        diag = Diag()
        print(diag.sendData([0x10, 0x02]))
        time.sleep(0.5)
        diag.securityAccessFastFBL()
        self.assertTrue(diag.securityAccessFastFBL(), False)

    @label(priority="P1")
    def test_000_test(self):
        print("test")
        self.assertFalse(False, False)

    @label(priority="P1")
    def test_2_readexcel(self):
        log.Log(Config_Parser("testfile/test_config.ini").get_config('Test_Files', 'diag_excel'))
        test = ExcelRead("testfile/test.xls")
        log.Log(test.readAll())

