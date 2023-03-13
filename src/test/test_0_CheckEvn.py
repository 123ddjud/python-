import unittest

from TestStart import label

@label(module = "TestEvn")
class Test_CheckEvn(unittest.TestCase):

    @label(priority="P0")
    def test_01_xxx(self):
        print("lalalala")
        self.assertTrue(True, True)

    @label(priority="P0")
    def test_02_xxx(self):
        print("hahaha")
        self.assertTrue(True,True)