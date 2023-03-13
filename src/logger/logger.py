import os,sys
sys.path.append(os.getcwd())
from parse import Config_Parser
import logging

class Logger():
    def __init__(self):
        self.__filename_path = os.path.join(os.getcwd(), "report", Config_Parser("./testfile/test_config.ini").get_config('Test_Report', 'txt_title'))
        self.__logger = logging.getLogger(self.__filename_path)
        self.__logger.setLevel(level=logging.DEBUG)

        self.__sh = logging.StreamHandler()
        self.__sh.setLevel(level=logging.DEBUG)
        self.__logger.addHandler(self.__sh)

        self.__fh = logging.FileHandler(filename=self.__filename_path, encoding="utf-8")
        self.__fh.setLevel(level=logging.DEBUG)
        self.__logger.addHandler(self.__fh)

    def get_Logger(self):
        return self.__logger

    def Log(self, string):
        formats = "%(asctime)s - [%(funcName)s-->line:%(lineno)d] - %(levelname)s:%(message)s"
        log_format = logging.Formatter(fmt=formats)
        self.__sh.setFormatter(log_format)
        self.__fh.setFormatter(log_format)
        self.get_Logger().info(string)


if __name__ == '__main__':
    log = Logger()
    log.Log("testststs")
    log.Log("dsgfvsdf")

