# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : BaseSettings.py
@desc: 
@Created on: 2021/1/6 12:02
"""
import os

# 基本文件夹路径的配置
BaseDIR = os.path.dirname(os.path.dirname(__file__))
EntranceDIR = os.path.join(BaseDIR,"Entrance\\")
StaticDIR =  os.path.join(EntranceDIR,"static\\")
ReportDIR =  os.path.join(StaticDIR,"Report\\")
LogsDIR = os.path.join(StaticDIR,"Logs\\")
PictureDIR = os.path.join(StaticDIR,"Picture\\")
AirResource = os.path.join(StaticDIR,"AirResource\\")
TestDataDIR = os.path.join(BaseDIR,"TestData\\")

# 手机的设备连接信息
RealMe = "android://127.0.0.1:5037/954f932f?cap_method=JAVACAP&&ori_method=ADBORI&&touch_method=ADBTOUCH"
MuMu = "android://127.0.0.1:5037/127.0.0.1:7555?cap_method=JAVACAP&&ori_method=ADBORI&&touch_method=ADBTOUCH"
InterFaceData = os.path.join(TestDataDIR,"Interface\\")



# 软件包名
cloudmusic ="com.netease.cloudmusic"


# 服务器账号名 和密码
USERNAME= "zs"
PD="123456"

import socket

# # 获取本机计算机名称
# hostname = socket.gethostname()
# # 获取本机ip
# ip = socket.gethostbyname(hostname)
ip = "10.10.10.119"
ipport = "http://" + ip + ":5000/"
# ipport = "http://testapp.cn1.utools.club/"
ipport_static_DIR = ipport+"static"
ipport_Report_DIR = ipport+'static/Report/'
AirResourceDIR = ipport+'static/AirResource'
# print(ipport)
NewEntranceDIR = EntranceDIR.replace("/","\\").replace("\\","\\\\")

if __name__ == '__main__':
    print(__file__)  # __file__ 指向 当前文件的路径
    print(os.path.dirname(__file__))
