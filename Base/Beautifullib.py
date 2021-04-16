# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : Beautifullib.py
@desc:  对BeautifulReport源码的重写
@Created on: 2021/1/7 15:09
"""
import base64
import json
import os
import platform
import sys
import time
from functools import wraps

from BeautifulReport.BeautifulReport import ReportTestResult, BeautifulReport
HTML_IMG_TEMPLATE = """
    <a href="data:image/png;base64, {}">
    <img src="data:image/png;base64, {}" width="800px" height="500px"/>
    </a>
    <br></br>
"""

class PATH:
    """ all file PATH meta """
    template_path = os.path.join(os.path.dirname(__file__), 'template')   # Base 下的  template文件夹
    config_tmp_path = os.path.join(template_path, 'template.html')  #  template文件夹下的  template.html

class DIYMakeResultJson:
    """ make html table tags """

    def __init__(self, datas: tuple):
        """
        init self object
        :param datas: 拿到所有返回数据结构
        """
        self.datas = datas
        self.result_schema = {}

    def __setitem__(self, key, value):
        """

        :param key: self[key]
        :param value: value
        :return:
        """
        self[key] = value

    def __repr__(self) -> str:
        """
            返回对象的html结构体
        :rtype: dict
        :return: self的repr对象, 返回一个构造完成的tr表单
        """
        keys = (
            'className',
            'methodName',
            'description',
            'html_path',
            'start_time',
            'spendTime',
            'status',
            'log',
        )
        # self.datas列表 每个数据： （class_name, method_name, method_doc, self.end_time, self.status, self.case_log）
        for key, data in zip(keys, self.datas):
            self.result_schema.setdefault(key, data)  # 生成一个字典  将keys和self.datas数据对应
        return json.dumps(self.result_schema)  # 字典转字符串


class DIYReportTestResult(ReportTestResult):
    @staticmethod
    def get_testcase_property(test) -> tuple:
        """
        接受一个test(case对象), 并返回一个test的class_name, method_name, method_doc属性
        :param test:
        :return: (class_name, method_name, method_doc) -> tuple
        """
        class_name = test.__class__.__qualname__  # 知道case属于哪一类
        method_name = test.__dict__['_testMethodName']  #拿取case名称 知道是哪一个case执行
        method_doc = test.__dict__['_testMethodDoc']   # 拿取case的描述信息
        html_path= test.__dict__.get('_html_path',"#")
        start_time=test.__dict__.get('_start_time',"跳过")
        return class_name, method_name, method_doc,html_path,start_time

    def stopTestRun(self, title=None) -> dict:
        """
            所有测试执行完成后, 执行该方法
        :param title:
        :return:
        """
        self.fields['testPass'] = self.success_counter  # 通过的case数量
        for item in self.result_list:  #result_list  每个case执行的结果  列表  itme  每个case执行的结果  （class_name, method_name, method_doc, self.end_time, self.status, self.case_log）
            """
            {
            'className',class_name
            'methodName',method_name
            'description',method_doc
            'spendTime',self.end_time
            'status', self.status
            'log',self.case_log
            }
            """
            item = json.loads(str(DIYMakeResultJson(item)))  # itme
            self.fields.get('testResult').append(item)
        self.fields['testAll'] = len(self.result_list)  # 执行过的case总数
        self.fields['testName'] = title if title else self.default_report_name # self.title
        self.fields['testFail'] = self.failure_count  # 失败的case数量
        self.fields['beginTime'] = self.begin_time  # 开始时间
        end_time = int(time.time())  # 获取当前时间戳变为整型
        start_time = int(time.mktime(time.strptime(self.begin_time, '%Y-%m-%d %H:%M:%S')))  # 把开始时间也转化成时间戳
        self.fields['totalTime'] = str(end_time - start_time) + 's'  # 计算所有case执行时间
        self.fields['testError'] = self.error_count  # 错误的case数量
        self.fields['testSkip'] = self.skipped   # 跳过的case数量
        return self.fields

class DIYBeautifulReport(DIYReportTestResult, PATH):
    img_path = 'img/' if platform.system() != 'Windows' else 'img\\'

    def __init__(self, suites):
        super(DIYBeautifulReport, self).__init__(suites)
        self.suites = suites
        self.report_dir = None
        self.title = '自动化测试报告'
        self.filename = 'report.html'

    def report(self, description, filename: str = None, report_dir='.', log_path=None, theme='theme_default'):
        """
            生成测试报告,并放在当前运行路径下
        :param report_dir: 生成report的文件存储路径    "测试报告"
        :param filename: 生成文件的filename        "report.html"
        :param description: 生成文件的注释
        :param theme: 报告主题名 theme_default theme_cyan theme_candy theme_memories
        :return :
        """
        if log_path:
            import warnings
            message = ('"log_path" is deprecated, please replace with "report_dir"\n'
                       "e.g. result.report(filename='测试报告_demo', description='测试报告', report_dir='report')")
            warnings.warn(message)

        if filename:
            #  防止用户忘记写后缀  给他拼接后缀
            self.filename = filename if filename.endswith('.html') else filename + '.html'

        if description:
            self.title = description

        self.report_dir = os.path.abspath(report_dir)   # BeautifulReport文件夹路径
        os.makedirs(self.report_dir, exist_ok=True)  # 创建BeautifulReport文件夹 存在即跳过
        self.suites.run(result=self)   # 执行套件内的所有case
        self.stopTestRun(self.title) #  所有测试执行完成后, 执行该方法  组装测试结果数据   存放到self.fields
        self.output_report(theme)  # theme  'theme_default'
        text = '\n测试已全部完成, 可打开 {} 查看报告'.format(os.path.join(self.report_dir, self.filename))
        print(text)

    def output_report(self, theme):
        """
            生成测试报告到指定路径下
        :return:
        """

        def render_template(params: dict, template: str):
            for name, value in params.items():
                name = '${' + name + '}'
                template = template.replace(name, value)
            return template

        template_path = self.config_tmp_path  #  #  template文件夹下的  template.html
        #  self.template_path  指向Base 下的  template文件夹 下的  'theme_default.json'
        with open(os.path.join(self.template_path, theme + '.json'), 'r') as theme:
            """
            render_params ={
                          "title": "color: #70AD47; font-size: 25px; font-weight: 700",
                          "sub-title": "color: #c4c4c4; font-size: 16px",
                          "color-banner": "#70AD47",
                          "color-info": "#555",
                          "color-pass": "#70AD47",
                          "color-skip": "#777777",
                          "color-fail": "#F25929",
                          "btn-expand": "#6ca745",
                          "btn-expand-active": "#568637",
                          "btn-collapse": "#F25929",
                          "btn-collapse-active": "#CA390C"
                          'resultData':  json字符串内容是  组装测试结果数据 
                            }
            """
            render_params = {
                **json.load(theme),  #
                'resultData': json.dumps(self.fields, ensure_ascii=False, indent=4)
            }

        # 判断是不是一个文件夹   如果不是 加个 /
        override_path = os.path.abspath(self.report_dir) if \
            os.path.abspath(self.report_dir).endswith('/') else \
            os.path.abspath(self.report_dir) + '/'

        with open(template_path, 'rb') as file:
            body = file.read().decode('utf-8')  #template.html内的文件信息
        #  根据 report_dir 和filename 拼接成一个报告的具体路径  并写入内容
        with open(override_path + self.filename, 'w', encoding='utf-8', newline='\n') as write_file:
            #
            html = render_template(render_params, body)
            write_file.write(html)

    @staticmethod
    def img2base(img_path: str, file_name: str) -> str:
        """
            接受传递进函数的filename 并找到文件转换为base64格式
        :param img_path: 通过文件名及默认路径找到的img绝对路径
        :param file_name: 用户在装饰器中传递进来的问价匿名
        :return:
        """
        pattern = '/' if platform != 'Windows' else '\\'

        with open(img_path + pattern + file_name, 'rb') as file:
            data = file.read()
        return base64.b64encode(data).decode()

    def add_test_img(*pargs):
        """
            接受若干个图片元素, 并展示在测试报告中
        :param pargs:
        :return:
        """

        def _wrap(func):
            @wraps(func)
            def __wrap(*args, **kwargs):
                img_path = os.path.abspath('{}'.format(BeautifulReport.img_path))
                os.makedirs(img_path, exist_ok=True)
                testclasstype = str(type(args[0]))
                # print(testclasstype)
                testclassnm = testclasstype[testclasstype.rindex('.') + 1:-2]
                # print(testclassnm)
                img_nm = testclassnm + '_' + func.__name__
                try:
                    result = func(*args, **kwargs)
                except Exception:
                    if 'save_img' in dir(args[0]):
                        save_img = getattr(args[0], 'save_img')
                        save_img(os.path.join(img_path, img_nm + '.png'))
                        data = BeautifulReport.img2base(img_path, img_nm + '.png')
                        print(HTML_IMG_TEMPLATE.format(data, data))
                    sys.exit(0)
                print('<br></br>')

                if len(pargs) > 1:
                    for parg in pargs:
                        print(parg + ':')
                        data = BeautifulReport.img2base(img_path, parg + '.png')
                        print(HTML_IMG_TEMPLATE.format(data, data))
                    return result
                if not os.path.exists(img_path + pargs[0] + '.png'):
                    return result
                data = BeautifulReport.img2base(img_path, pargs[0] + '.png')
                print(HTML_IMG_TEMPLATE.format(data, data))
                return result

            return __wrap

        return _wrap