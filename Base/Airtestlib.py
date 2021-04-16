# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : Airtestlib.py
@desc: 用来存放修改过的airtest代码
@Created on: 2021/1/5 15:41
"""
import io
import json
import os
import shutil

import jinja2
from airtest.cli.info import get_script_info
from airtest.core.api import connect_device
from airtest.core.helper import G
from airtest.core.settings import Settings as ST
from airtest.report.report import LogToHtml, nl2br, timefmt, LOGGING
from airtest.utils.compat import script_dir_name
from Base.BaseSettings import AirResourceDIR, NewEntranceDIR, ipport, AirResource


def only_auto_setup(basedir=None, devices=None, project_root=None, compress=None):
    """
    单纯的建立设备连接
    Auto setup running env and try connect android device if not device connected.

    :param basedir: basedir of script, __file__ is also acceptable.  __file__
    :param devices: connect_device uri in list.
    :param logdir: log dir for script report, default is None for no log, set to `True` for <basedir>/log.
    :param project_root: project root dir for `using` api.
    :param compress: The compression rate of the screenshot image, integer in range [1, 99], default is 10
    """
    if basedir:
        if os.path.isfile(basedir):
            basedir = os.path.dirname(basedir)
        if basedir not in G.BASEDIR:
            G.BASEDIR.append(basedir)
    if devices:
        for dev in devices:
            connect_device(dev)
    if project_root:
        ST.PROJECT_ROOT = project_root
    if compress:
        ST.SNAPSHOT_QUALITY = compress

def only_set_logdir(logdir):

    if os.path.exists(logdir):
        shutil.rmtree(logdir)
    os.makedirs(logdir,exist_ok=True)
    ST.LOG_DIR = logdir
    G.LOGGER.set_logfile(os.path.join(ST.LOG_DIR, ST.LOG_FILE))


def DIYsimple_report(filepath, logpath=True, logfile="log.txt", output="log.html",case_info={}):
    """
    :param filepath: __file__  文件路径
    :param logpath:  默认为True   LogsDIR + kwargs["logname"]  我们设定的日志文件夹输出地址
    :param logfile: 默认 log.txt   产生的日志文件夹的路径下的log.txt
    :param output:  默认  log.html   我们设定的报告输出地址    ReportDIR + kwargs["logname"] + ".html"
    :return:
    """
    path, name = script_dir_name(filepath)  #path  传入的文件的上一级目录  name 文件名
    if logpath is True:
        logpath = os.path.join(path, "log")
    rpt = DIYLogToHtml(path, logpath, logfile=logfile, script_name=name,static_root=AirResourceDIR,)
    rpt.report("log_template.html", output_file=output,case_info=case_info)   # HTML_TPL  "log_template.html"


class DIYLogToHtml(LogToHtml):
    def report(self, template_name="log_template.html", output_file=None, record_list=None,case_info={}):
        """
        Generate the report page, you can add custom data and overload it if needed
        :param template_name: default is HTML_TPL     # HTML_TPL  "log_template.html"
        :param output_file: The file name or full path of the output file, default HTML_FILE   设定的报告输出地址
        :param record_list: List of screen recording files     None
        :return:
        """
        if not self.script_name:
            path, self.script_name = script_dir_name(self.script_root)

        if self.export_dir:
            self.script_root, self.log_root = self._make_export_dir()
            # output_file可传入文件名，或绝对路径
            output_file = output_file if output_file and os.path.isabs(output_file) \
                else os.path.join(self.script_root, output_file or "log.html")
            if not self.static_root.startswith("http"):
                self.static_root = "static/"

        if not record_list:
            record_list = [f for f in os.listdir(self.log_root) if f.endswith(".mp4")]  # [ ]
        # output_file   设定的报告输出地址   record_list  [ ]
        # data 拿到的是一个数据字典
        data = self.report_data(output_file=output_file, record_list=record_list,case_info=case_info)
        return self._render(template_name, output_file, **data)


    @staticmethod
    def _render(template_name, output_file=None, **template_vars):
        """ 用jinja2渲染html"""
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(AirResource),
            extensions=(),
            autoescape=True
        )
        env.filters['nl2br'] = nl2br
        env.filters['datetime'] = timefmt
        template = env.get_template(template_name)
        html = template.render(**template_vars)

        if output_file:
            with io.open(output_file, 'w', encoding="utf-8") as f:
                f.write(html)
            LOGGING.info(output_file)

        return html


    def report_data(self, output_file=None, record_list=None,case_info = {}):
        """
        Generate data for the report page
        :param output_file: The file name or full path of the output file, default HTML_FILE
        :param record_list: List of screen recording files
        :return:
        """
        self._load()   # 拿log数据
        steps = self._analyse()  # 处理log 数据  #返回一个列表 每个数据就是解析后的可渲染的dict

        script_path = os.path.join(self.script_root, self.script_name)  #运行的文件名  __file__
        #info 字典 { script_name 文件名    script_path 文件完整路径  文件中的__author__  title, desc}
        info = json.loads(get_script_info(script_path)) #拿到文件的相关信息
        info["title"] = case_info.get("title", "")
        info["author"] = case_info.get("author", "")
        info["desc"] = case_info.get("casedesc", "")
        # info["netpath"] = info['path'].replace(NewEntranceDIR,ipport)
        records = [os.path.join("log", f) if self.export_dir
                   else os.path.abspath(os.path.join(self.log_root, f)) for f in record_list]

        if not self.static_root.endswith(os.path.sep): #  为了支持服务器 http://192.168.56.1:5000/static/AirResource// \
            self.static_root = self.static_root.replace("\\", "/")
            self.static_root += "/"

        data = {}
        data['steps'] = steps  #  #返回一个列表 每个数据就是解析后的可渲染的dict
        data['name'] = self.script_root  #  文件的上一级目录
        data['scale'] = self.scale # 缩放比例
        data['test_result'] = self.test_result  # 测试结果
        data['run_end'] = self.run_end
        data['run_start'] = self.run_start
        data['static_root'] = self.static_root
        data['lang'] = self.lang
        data['records'] = records  # 【】
        data['info'] = info  #info 字典 { script_name 文件名    script_path 文件完整路径  文件中的__author__  title, desc}
        data['log'] = self.get_relative_log(output_file)
        data['console'] = self.get_console(output_file)
        # 如果带有<>符号，容易被highlight.js认为是特殊语法，有可能导致页面显示异常，尝试替换成不常用的{}
        info = json.dumps(data).replace("<", "{").replace(">", "}")
        # info.replace(r"D:\\Pycharm\\PythonProject\\app33\\AutoTest\\","http://192.168.56.1:5000/static/")
        info = info.replace(NewEntranceDIR,ipport)
        data['data'] = info  # 字符串 data内容s
        return data  #字典