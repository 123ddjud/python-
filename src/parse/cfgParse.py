import os,sys
sys.path.append(os.getcwd())
#configparser用于配置文件解析，可以解析特定格式的配置文件
import configparser

class Config_Parser():
    def __init__(self, configfile):
        self.__configfile = configfile
        #初始化实例，并读取配置文件
        self.__cf = configparser.ConfigParser()
        self.__cf.read(self.__configfile)

    #  section:节点    item：键值
    def get_config(self, section, item):
        value = None
        try:
            #读取对应节点、键值的值
            value = self.__cf[section][item]
        except BaseException as e:
            print("get_config error %s ---> %s: %s" % (section, item, e))
        return value

    def write_config(self, section, item, value):
        if value is None:
            return False
        elif value == self.get_config(section, item):
            return True
        else:
            try:
                #如果config文件中没有对应节点，则添加对应节点
                if not self.__cf.has_section(section):
                    self.__cf.add_section(section)
                #设置对应节点、键值的值
                self.__cf.set(section, item, value)
                #将新添加的节点写入config文件中
                with open(self.__configfile, 'w+') as f:
                    self.__cf.write(f)
            except BaseException as e:
                print("config set fail %s ---> %s : %s"% (section,item,e))
                return False
        return True
