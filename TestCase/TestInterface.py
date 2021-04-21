# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : TestInterface.py
@desc: 
@Created on: 2021/4/19 15:45
"""
import time
import unittest
import ddt
import requests
from jsonpath import jsonpath

from Base.BaseSettings import InterFaceData
from Base.PublicFunc import get_interface_data, OptionsException, InterfaceVariable


@ddt.ddt
class TestInterface(unittest.TestCase):

    @ddt.data(*get_interface_data())
    def test_all_interface(self,case_detail):

        # 组织报告上要显示的数据
        self.__class__.__qualname__ =case_detail.get('class',"class undefined")
        self.__dict__['_testMethodName'] = case_detail.get('name','func undefined')
        self.__dict__['_testMethodDoc'] = case_detail.get('desc',"desc undefined")
        self.__dict__['_start_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # 获取测试case中的请求部分信息
        request_data = case_detail['request']

        # 对 request_data的数据进行预处理
        for item in  list(request_data):

            if item=="method":
                # 对请求方法支持用户输入大小写
                request_data[item] = request_data[item].lower()

            if item in ["data","json","params","headers"]:
                for item2,values2 in request_data[item].items():
                    # 对需要使用 变量的数据 获取变量
                    if isinstance(values2,str) and values2.startswith("$"):
                        request_data[item][item2]=getattr(InterfaceVariable,item2)

            if item == "cookies":
                if isinstance(request_data[item], str) and request_data[item].startswith("$"):
                    request_data[item]=getattr(InterfaceVariable,request_data[item][1:])

        # 发送请求

        res = requests.request(**request_data)

        # 查看是否有要保存的 接口关联性数据
        if case_detail.get('variable'):
            # 获取要保存的数据 先检查文档是否已经存入数据：
            for item,values in case_detail['variable'].items():
                if values.startswith("$."):
                    v = jsonpath(res.json(), values)   # jsonpath 获取结果默认列表返回
                    if len(v) == 1:
                        setattr(InterfaceVariable,item,v[0])
                    else:
                        setattr(InterfaceVariable, item, v)
                elif values.startswith("response."):
                    # 获取响应内容的数据
                    a= getattr(res, values.split(".")[1])
                    setattr(InterfaceVariable,item,a)
                else:
                    # 设置变量为自定义的纯字符串
                    setattr(InterfaceVariable,item,values)

        # 获取断言数据
        checking_info = case_detail['checking']

        if checking_info['type']=="json":
            for i, v in checking_info['assert'].items():
                if i == "eq":
                    for i2, v2 in v.items():
                        v = jsonpath(res.json(), i2)
                        if len(v)==1:
                            self.assertEqual(v2, v[0])
                        else:
                            self.assertIn(v2, v)
                elif i == "in":
                    for i2, v2 in v.items():
                        v = jsonpath(res.json(), i2)
                        if len(v)==1:
                            self.assertIn(v2,v[0])
                        else:
                            self.assertIn(v2, v)
                else:
                    raise OptionsException("checking里面的 assert目前只支持in 和eq，请按规则写入")

        elif checking_info['type'] in ["text","html"]:
            for i, v in checking_info['assert'].items():
                if i == "eq":
                    self.assertEqual(v, res.text)
                elif i == "in":
                    self.assertIn(v, res.text)
                else:
                    raise OptionsException("checking里面的 assert目前只支持in 和eq，请按规则写入")
        else:
            raise OptionsException("checking里面的 type目前只支持json 和text，请按规则写入")

if __name__ == '__main__':
    unittest.main()