# 1. 项目部署准备

python 3.6以上版本

pip install airtest  -i https://mirrors.aliyun.com/pypi/simple/

pip install pocoui

pip install BeautifulReport==0.1.3

pip install flask==1.1.2

# 2.项目目录结构

- Base  存放公共文件 基础文件

  - template  beautifulReport的报告文件 不要动

  - Airtestlib  对airtest源码修改的内容  不要动
  
  - Page 存放页面对象模型

  - Beautifullib  对BeautifulReport源码修改的内容 不要动

  - Basesettings   基本配置

  - PublicFunc    用来存放公共函数

    - ```
      get_parameter  在每个case上添加该装饰器  作用: 异常捕获 自动生成报告
      ```

    - 

- Entrance  在线服务器入口

  - static  静态服务器资源
    - AirResource  airtest相关资源放到静态服务器  不要动
    - Logs  存放的每个case日志  会自动产生  也不要动
    - Picture  case中要用到的图片 全都放在该文件夹下
    - Report  产出的case报告  会自动生成  不要动
  - templates  模板资源
  - run.py  服务器启动入口文件   执行该文件 启动服务器

- Test  用于自己测试  

- TestCase  所有写的case存放在该目录下 建议 以模块 命名文件  多个模块 新建多个文件

- TestSuite  套件文件夹

# 3. 框架使用步骤

## 1. BaseSettings文件

- 修改手机的设备信息

- 修改ip地址信息

  ![image-20210331094053437](https://woniumd.oss-cn-hangzhou.aliyuncs.com/test/zhangjing/20210331094053.png)

## 2. PublicFunction 文件

- get_parameter 函数

  ![image-20210331094237829](https://woniumd.oss-cn-hangzhou.aliyuncs.com/test/zhangjing/20210331094237.png)

- ![image-20210331094459258](https://woniumd.oss-cn-hangzhou.aliyuncs.com/test/zhangjing/20210331094459.png)

## 3. 模仿demo 自己定义case文件

## 4. 修改套件文件 导入自己编写的case

# 4. 版本历史

## 1.0 版本

实现一个报告平台 用来在线展示代码中运行好的case报告

## 1.1 版本

 去除报告详情页面的logo 可以在页面底部添加广告(暂时还没有广告logo)

## 1.2 版本

 实现单例 避免 写了多个文件重复启动app 浪费时间
 
 ## 如果您觉得这个产品对您有用，您可以捐助下我，让我有理由继续下去，非常感谢。
![image-20210416143755979](https://woniumd.oss-cn-hangzhou.aliyuncs.com/test/zhangjing/20210416143756.png)
![image-20210416143919108](https://woniumd.oss-cn-hangzhou.aliyuncs.com/test/zhangjing/20210416143919.png)
 
 ## 当然你也可以关注加星支持 非常感谢！！！