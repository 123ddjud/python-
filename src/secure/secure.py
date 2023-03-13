import os,sys
sys.path.append(os.getcwd())
from ctypes import *

class Security():
    def __init__(self):
        self.__firewall_dll = None

    def get_Firewall_PublicKey(self):
        if os.path.exists(".\Firewall.dll"):
            self.__firewall_dll = WinDLL(".\Firewall.dll")
        else:
            self.__firewall_dll = None

        temp = []
        if self.__firewall_dll != None:
            length = c_int()
            key = (c_ubyte * 4)()
            ret = self.__firewall_dll.GetPublicKey(key, byref(length))
            for _ in key:
                temp.append(_)
            return temp
        return None

    def get_Firewall_IDData(self, seed_data = []):
        if self.__firewall_dll != None:
            seed_length = 4
            SeedData = (c_ubyte * seed_length)()
            for _ in range(0, seed_length):
                SeedData[_] = (c_ubyte(seed_data[_]))
            IDData = (c_ubyte * 4)()
            IDlength = c_int()
            ret1 = self.__firewall_dll.SeedDecryptAndIDEncrypt(SeedData, seed_length, IDData, byref(IDlength))
            data = []
            for _ in IDData:
                data.append(_)
            return data
        return None

#    securityConstant default: SAIC GW APP
#    SAIC GW FBL: securityConstant = 0xDBC8812B
    @classmethod
    def get_securityAccessKey_SAIC(self, seed_data = [], securityConstant = 0xCDCF543E):
        seed = ""
        for _ in seed_data:
            seed = seed + format(_, "02X")
        SECURITYCONSTANT = securityConstant
        wTemp = 0
        wTop31Bits = 0
        wLastSeed = 0
        wSeed = int(seed, 16)
        wLastSeed = wSeed
        temp = ((SECURITYCONSTANT & 0x00000800) >> 10) | ((SECURITYCONSTANT & 0x00200000) >> 21)
        if temp == 0:
            wTemp = (wSeed & 0xff000000) >> 24
        elif temp == 1:
            wTemp = (wSeed & 0x00ff0000) >> 16
        elif temp == 2:
            wTemp = (wSeed & 0x0000ff00) >> 8
        elif temp == 3:
            wTemp = wSeed & 0x000000ff
        SB1 = (SECURITYCONSTANT & 0x000003FC) >> 2
        SB2 = ((SECURITYCONSTANT & 0x7F800000) >> 23) ^ 0xA5
        SB3 = ((SECURITYCONSTANT & 0x001FE000) >> 13) ^ 0x5A
        iterations = ((wTemp ^ SB1) & SB2) + SB3
        for _ in range(iterations):
            wTemp = ((wLastSeed & 0x40000000) // 0x40000000) ^ \
                    ((wLastSeed & 0x01000000) // 0x01000000) ^ \
                    ((wLastSeed & 0x1000) // 0x1000) ^ ((wLastSeed & 0x04) // 0x04)
            wLSBit = wTemp & 0x00000001
            wLastSeed = wLastSeed << 1
            wTop31Bits = wLastSeed & 0xFFFFFFFE
            wLastSeed = wTop31Bits | wLSBit
        if SECURITYCONSTANT & 0x00000001:
            wTop31Bits = ((wLastSeed & 0x00FF0000) >> 16) | \
                         ((wLastSeed & 0xFF000000) >> 8) | \
                         ((wLastSeed & 0x000000FF) << 8) | \
                         ((wLastSeed & 0x0000FF00) << 16)
        else:
            wTop31Bits = wLastSeed
        wTop31Bits = wTop31Bits ^ SECURITYCONSTANT
        key = []
        key.append((wTop31Bits & 0xFF000000) >> 24)
        key.append((wTop31Bits & 0x00FF0000) >> 16)
        key.append((wTop31Bits & 0x0000FF00) >> 8)
        key.append(wTop31Bits & 0x000000FF)
        return key


# from config import Config_Parser
# if __name__ == '__main__':
#     print(Config_Parser("testfile/test_config.ini").get_config('Test_Report', 'txt_title'))