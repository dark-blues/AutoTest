# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : run.py
@desc: 
@Created on: 2021/1/8 16:27
"""

from flask import Flask, request, render_template, redirect, url_for, session, jsonify

from Base.BaseSettings import USERNAME, PD

app = Flask(__name__)
app.secret_key="woniuxueyuan"
app.config["JSON_AS_ASCII"]=False
@app.route("/")
def index():
    username = session.get('username')
    if username==USERNAME:
        #到首页后 访问静态文件（我们生成好的报告页面）
        return app.send_static_file('report.html')
    else:
        return redirect(url_for('login'))

@app.route("/login",methods=["GET","POST"])
def login():
    # 根据 请求方法判断
    # GET 请求显示登陆页面
    if request.method == "GET":
        return render_template("login.html")
    else:
        # POST  说明提交用户名和密码
        # 接受用户传过来的用户名和密码
        username = request.form.get("username")
        # 判断数据库有没有该用户
        if username == USERNAME:
            # 有用户 判断密码是否正确
            password = request.form.get("password")
            if password ==PD:
                # 提示登录成功返回首页
                session['username']=username
                return redirect(url_for('index'))
            else:
                # 访问模板页面
                return render_template("login.html", errmsg="密码错误")
        # 没有查到用户  提示用户不存在
        else:
            return render_template("login.html",errmsg="用户名不存在")

@app.route("/favicon.ico")
def getfavicon():
    return app.send_static_file("timg.jpg")

if __name__ == '__main__':
    import socket

    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    ip = socket.gethostbyname(hostname)
    ipport = "http://" + ip + ":5000/"
    print(ipport)
    app.run(host="0.0.0.0",port=5000,debug=True)