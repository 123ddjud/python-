import wrapt
import unittest
import os,sys,time
sys.path.append(os.getcwd())
from parse import Config_Parser
from HTMLTestRunner import HTMLTestRunner

cfgfile = os.path.join(os.getcwd(), 'testfile', "test_config.ini")
projects = Config_Parser(cfgfile).get_config('Test_Filter', 'project')
functions = Config_Parser(cfgfile).get_config('Test_Filter', 'module')
prioritys = Config_Parser(cfgfile).get_config('Test_Filter', 'priority')

def label(**kkargs):

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        print('test ------ %s' % (wrapped.__name__))
        return wrapped(*args, **kwargs)

    mantch_project = True
    if 'project' in kkargs:
        mantch_project = False
        proj = kkargs['project']
        for _ in proj.split():
            for p in projects.split():
                if _.strip().lower() == p.strip().lower():
                    mantch_project = True
            if mantch_project:
                break

    mantch_module = True
    if 'module' in kkargs:
        mantch_module = False
        func = kkargs['module']
        for fun in functions.split():
            if func.strip().lower() == fun.strip().lower():
                mantch_module = True
                break

    mantch_priority = True
    if 'priority' in kkargs:
        mantch_priority = False
        pri = kkargs['priority']
        for prio in prioritys.split():
            if pri.strip().lower() == prio.strip().lower():
                mantch_priority = True
                break
    if mantch_project and mantch_module and mantch_priority:
        return wrapper
    else:
        return unittest.skip('not match')

class TestRunner():
    def __init__(self, runner = None, test_case_dir = ""):
        self.__testx = unittest.TestSuite()
        self.__dir = test_case_dir
        self.__runner = runner

    def __get_case(self, t):
        if isinstance(t, unittest.TestSuite) and t.countTestCases() != 0:
            for _ in t:
                self.__get_case(_)
        elif isinstance(t, unittest.TestCase):
            self.__testx.addTest(t)
        else:
            pass

    def run(self):
        discover = unittest.TestLoader().discover(self.__dir, pattern="test_*.py")
        self.__get_case(discover)
        self.__runner.run(self.__testx)
        # self.__runner = unittest.TextTestRunner()
        # self.__runner.run(discover)

if __name__ == '__main__':
    rep_name = Config_Parser(cfgfile).get_config('Test_Report', 'html_title')
    report_name =rep_name  + time.strftime('_%F-%H-%M-%S.html')
    report_path = os.path.join(os.getcwd(), 'report', report_name)
    with open (report_path, "wb" ) as f:
        runner = HTMLTestRunner(stream=f, title=report_name, verbosity=2)
        testRunner = TestRunner(runner= runner, test_case_dir="./test")
        testRunner.run()
    

