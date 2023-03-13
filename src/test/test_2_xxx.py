import unittest

from TestStart import label

@label(module = "test")
class Test_Others(unittest.TestCase):

    @label(project="SAIC_TBOX_FBL")
    def test_01_xxx(self):
        print("lalalala")

    @label(priority='P2')
    def test_02_xxx(self):
        print("hahaha")