# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : PublicFunc.py
@desc: 
@Created on: 2021/1/8 14:16
"""
import json
import logging
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps

import yaml
from airtest.cli.parser import cli_setup
from airtest.core.api import *
import unittest
from Base.Airtestlib import only_set_logdir, only_auto_setup, DIYsimple_report
from Base.BaseSettings import LogsDIR, ReportDIR, ipport, ipport_Report_DIR, cloudmusic, RealMe, InterFaceData


def get_parameter(file,logname,**dkwargs):
    """
    装饰器接收参数
    :param file:  文件地址  必传 传固定值 __file__ 即可
    :param logname:  日志文件夹名称 必传  建议跟case名称保持一致 要求英文 但是不允许出现同名case名称
    还支持以下参数  使用关键字传参形式传递
    :param casedesc:  case描述信息
    :param title:  title  case的标题 不填的话 默认是logname
    :param author:  author case的作者信息
    :return:
    """
    def outer(func):
        @wraps(func)
        def inner(self,*args, **kwargs):
            #
            dkwargs.setdefault('title',logname)
            self.__dict__['_testMethodDoc'] = dkwargs.get('casedesc',"")
            self.__dict__['_start_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            only_set_logdir(LogsDIR + logname)
            try:
                arg = func(self,*args, **kwargs)
            except Exception as e:
                print("18", e)
                log(e, snapshot=True)  # 让airtest报告能识别出错误
                raise e   # 让unittest能识别出错误
            finally:
                DIYsimple_report(file, logpath=LogsDIR+logname, output=ReportDIR +logname+".html",case_info=dkwargs)
                # self.__dict__['_html_path'] = ReportDIR +logname+".html"
                self.__dict__['_html_path'] = ipport_Report_DIR +logname+".html"

                # 这里添加 是否回到首页的判断逻辑
                # while not self.poco(text="歌单").exists():
                #     if self.poco(text="发现").exists():
                #         self.poco(text="发现").click()
                #     else:
                #         keyevent("BACK")

                while not (self.poco(text="歌单").exists() and self.poco(text="每日推荐").exists()):
                    keyevent("BACK")

            return arg
        return inner
    return  outer

class GetPoco():
    poco = None

    @classmethod
    def get_poco(cls):
        print(cls.poco,"-----------------72")
        # if not  <poco.drivers.android.uiautomation.AndroidUiautomationPoco object at 0x00000197FC0E5A58>
        if not cls.poco:
            logger = logging.getLogger("airtest")
            logger.setLevel(logging.ERROR)

            from poco.drivers.android.uiautomation import AndroidUiautomationPoco
            cls.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

            if not cli_setup():
                only_auto_setup(__file__, devices=[
                    RealMe
                ])
            stop_app(cloudmusic)  # 防止测试的时候 手机上 该应用还在后台运行
            sleep(1)
            # 这里填写要测试的app包名
            start_app(cloudmusic)
            sleep(2)
        return cls.poco

def poco(fangfa,dingwei):
    poco_obj = GetPoco.poco
    if fangfa=="text" or fangfa is 1:
        return poco_obj(text=dingwei)
    elif fangfa == "name" or fangfa is 2:
        return poco_obj(dingwei)
    else:
        print("目前只支持 text 和 name")

class SetUpClass(unittest.TestCase):

    """初始化类"""
    def setUp(self) -> None:
        # only_set_logdir(LogsDIR+"ranklistlog")
        pass

    @classmethod
    def setUpClass(cls) -> None:
        cls.poco = GetPoco.get_poco()
    def tearDown(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

def send_email(email_Subject="测试报告结果",  received_Email=["1576094876@qq.com"], mailserver="smtp.qq.com",
               userName_SendEmail='1576094876@qq.com', userName_AuthCode='zixlefqyrwmwbagg',file_path="", filename="",):
    mailserver = mailserver
    userName_SendEmail = userName_SendEmail
    userName_AuthCode = userName_AuthCode
    received_Email = received_Email

    # 创建邮件对象
    msg = MIMEMultipart()
    msg["Subject"] = Header(email_Subject, 'utf-8')
    msg["From"] = userName_SendEmail
    msg["To"] = ",".join(received_Email)

    # 发送普通文本
    content="尊敬的用户报告已经生成，请前往 %s   查看"%ipport
    html_content = MIMEText(content, 'plain', 'utf-8')
    msg.attach(html_content)

    # 邮件中发送附件
    # content = open(file_path, 'rb').read()
    # att = MIMEText(content, "base64", "utf-8")
    # att["Content-Type"] = "application/octet-stream"  # 一种传输形式
    # att["Content-Disposition"] = "attachment;filename=%s" % filename
    # msg.attach(att)

    smtp = smtplib.SMTP_SSL(mailserver)  # 创建客户端
    smtp.login(userName_SendEmail, userName_AuthCode)
    smtp.sendmail(userName_SendEmail, ",".join(received_Email), msg.as_string())
    smtp.quit()

class OptionsException(Exception):
    '''自定义的异常类'''
    def __init__(self, info):
        self.info = info

    def __str__(self):
        return f"{self.info}"

class InterfaceVariable:
    # 接口自动化过程中要来存储 具有相关连性接口的数据
    # 千万别给我删了
    pass

def filename_to_hump(filename):
    """
    将文件名转换成驼峰写法
    filename: 文件路径
    """
    basefile = os.path.basename(filename).lower() # 只获取文件名的小写
    fileprefix = basefile[:basefile.rfind(".")] # 获取文件前缀
    if len(fileprefix.split("_"))==1: # 说明名称内没有_
        filename = "Test"+fileprefix[4:].capitalize()
    else:
        filename = "".join([i.capitalize() for i in fileprefix.split("_")])

    return filename


def get_interface_data(filenamelist:list=None):
    # 获取所有符合条件的文件
    if filenamelist:
        filenamelist = [InterFaceData+filename for filename in filenamelist]
    else:
        filenamelist = os.listdir(InterFaceData)
        filenamelist = [InterFaceData + filename for filename in filenamelist if filename.lower().startswith("test")]

    all_data = []
    for filename in filenamelist:
        # 获取文件的驼峰写法 用于给里面的数据进行 类名赋值
        class_name =  filename_to_hump(filename)

        if filename.endswith(".json"):
            with open(filename,"r",encoding='utf-8') as f:
                data = json.load(f)

        elif filename.endswith(".yaml"):
            with open(filename, "r",encoding='utf-8') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        for i in data:
            if not i.get("class"):
                i["class"] =class_name
        all_data += data

    return all_data

if __name__ == '__main__':
    get_interface_data()
    #
    # filename_to_hump(r"D:\Pycharm\AutoTest\TestData\Interface\test_Gold_add.json")