from uds import Uds
from threading import RLock
from secure import Security
from parse import Config_Parser

secure_dict = {
    "SAIC_GW_APP":0xDC8FE1AE,
    "SAIC_GW_FBL":0xDBC8812B,
    "SAIC_TBOX_APP":0x00000000,
    "SAIC_TBOX_FBL":0xCDCF543E
}

class Diag():
    udses = {}
    def __init__(self, uds_name="pdiag_uds", reqid=0x711, resid=0x719, interface="CANoe", channel="0" ,connect = "HSCAN5"):
        self.lock = RLock()
        self.__uds_name = uds_name
        self.__interface = interface
        self.__channel = channel
        self.__connect = connect
        self.__reqId = reqid
        self.__resId = resid
        self.__uds = None
        self.setUds()

    def get_reqId(self):
        return self.__reqId

    def get_resId(self):
        return self.__resId

    def setUds(self):
        try:
            self.__uds = Uds(reqId=self.__reqId,
                             resId=self.__resId,
                             interface=self.__interface,
                             channel=self.__channel,
                             connected=self.__connect,
                             P2_CAN_Client=2,
                             P2_CAN_Server=2)
        except Exception as e:
            self.__uds = None
            print("UDS: %s set fail " % str(e))
        if self.__uds:
            self.udses[self.__uds_name] = self.__uds

    def getUds(self):
        if self.__uds_name not in self.udses:
            self.setUds()
        if self.__uds_name in self.udses:
            return self.udses[self.__uds_name]
        else:
            return None

    def close_connection(self):
        uds = self.getUds()
        if uds:
            uds.disconnect()
        if self.__uds_name in self.udses:
            del self.udses[self.__uds_name]

    def sendData(self, data=[0x10,0x01], responseRequired = True):
        if not self.getUds():
            return None
        with self.lock:
            if responseRequired:
                try:
                    res = self.getUds().send(data)
                    return res
                except Exception as e:
                    print("Tx: %s" % str(e))
            else:
                self.getUds().send(data, responseRequired=False)
        return None

    def securityAccessFastFBL(self):
        project_temp =  Config_Parser("./testfile/test_config.ini").get_config('Test_Filter', 'project')
        securityConstant = 0
        for _ in secure_dict:
            if _ == project_temp:
                securityConstant = secure_dict[_]
                break
        if "SAIC" in project_temp:
            res = self.sendData([0x27, 0x05])
            if res != None:
                if res[0] == 0x67 and res[1] == 0x05:
                    keylist = [0x27, 0x06] + Security.get_securityAccessKey_SAIC(seed_data=res[-4:], securityConstant=securityConstant)
                    res = self.sendData(keylist)
                    print(res)
                    if res != None:
                        if res[0] == 0x67 and res[1] == 0x06:
                            return True
        elif "xxx" in project_temp:
            pass
        return False

