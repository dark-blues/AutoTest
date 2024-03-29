# 1. 项目部署准备

python 3.6以上版本

pip install airtest  -i https://mirrors.aliyun.com/pypi/simple/

pip install pocoui

pip install BeautifulReport==0.1.3

pip install flask==1.1.2

pip install PyYAML==5.4.1

pip install ddt==1.4.2

pip install jsonpath==0.82
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
实现移动端自动化 让功能测试人员 通过airtestIDE录制脚本，然后移植到项目内，就能让功能测试人员也参与到移动端自动化的过程

实现一个报告平台 用来在线展示代码中运行好的case报告

## 1.1 版本

 去除报告详情页面的logo 可以在页面底部添加广告(暂时还没有广告logo)

## 1.2 版本

 实现单例 避免 写了多个文件重复启动app 浪费时间
<<<<<<< HEAD

## 2.0 版本
新增接口自动化框架 支持yaml格式或者json格式编写接口自动化测试用例
用户不需要关注代码逻辑，只要按要求编写json文件或者yaml文件，让不会代码的人也能参与到自动化测试中

TestCase目录下新建TestInterface.py文件 该文件就是用来解析接口文档的数据，然后发送请求解析
对于用户来说 只需要修改自己把test.json换成自己的接口文档就可以了
![image-20210420102107352](https://woniumd.oss-cn-hangzhou.aliyuncs.com/test/zhangjing/20210420102107.png)
提供test.json和test.yaml作为模板
接口文件编写规则：
- name表示测试的函数名称 用于后期报告上显示

- class表示测试的接口类别 用于后期报告作过滤

- desc 表示case的描述信息 用于报告显示

- request 表示这个接口 的请求构成
    
    - url 填写接口的请求地址
    - method 填写接口的请求方式 忽略大小写
    - data 接口的表单数据  
    - headers 接口请求头部信息数据
    - params 接口查询字符串信息数据
    - 如果中间要涉及到前置接口产生的结果 使用 $变量名表示 
    - 整个流程可以让测试人员用postman测完，然后把这个接口转成json信息或yaml信息即可
    
- variable 接口流程结束 需要保存的变量 方便后面的接口调用使用

    - 以键值对形式保存数据 键表示变量名 值的话支持对json返回的数据解析，支持纯变量赋值，支持对response响应的内容获取数据
    - 支持对当前json数据解析 使用 $.表示返回的json数据，支持.语法  内置其实采用的jsonpath解析。$.data.token表示返回内容下的data数据下的token值  可参考文档 https://blog.csdn.net/nd211314555/article/details/88426529
    - 支持对response解析获取 如response.cookies获取响应的cookie。response.text获取响应的文本内容
    - 如果要使用常量 就直接 写即可

- checking 用来做断言的

    - type 目前支持对 json,text,html 内容作断言，根据响应内容的不同自己选择不同类型

    - assert表示断言，支持两种eq和in。 eq表示判断值是否相等，in表示判断值是否存在

    - json的话以及支持jsonpath语法 

        ```json
        "assert": {
            "eq": {
                "$.code": 200,
                "$.message": "成功!",
                "$.result.weekday": "星期二"
            },
            "in": {
                "$.result.weekday": "星期"
            }
        # 表示 返回的响应内容的 code =200，message为成功!，result下的weekday 为星期二 
        ```

    - text/html 直接就是判断文本内容

        ```json
        "assert": {
          "eq": "already-added",
          "in":  "added"
          }
         # 表示响应的文本内容 等于already-added 存在added
        ```
## 2.1 版本
修改如果jsonpath获取的数据是个列表 也只会拿到第一个数据的bug

## 2.2 版本
1. 支持对多个接口文档的执行
![image-20210421131944754](https://woniumd.oss-cn-hangzhou.aliyuncs.com/test/zhangjing/20210421131944.png)
get_interface_data()函数不传参数 则读取TestData目录下Interface文件下所有的以'test'(忽略大小写)开头的接口文档数据并执行

2. 支持同时传入多个文件，如果你想只执行多个接口文档 可以 get_interface_data(["test.json","test.yaml"]) 传入列表，列表的元素就是interface的文件名

3. 接口文档编写 时 class可以不填 默认以文件名的驼峰写法作为类名。如test_gold.json的类名就是TestGold

目的：以上更新的目的是 实际中一个项目可能有多个测试人员负责，一个测试人员负责一个模块，那么这个测试人员只要写自己的接口文档并放到Interface目录下即可。每个测试人员不需要共用一个接口文件了。
默认运行Interface目录下所有test开头的接口文档。可以人为指定执行具体某些文档，更加人性化

## 2.3 版本
修复 开始时间是跳过的bug

## 2.4  版本
对于响应是json数据时，会有测试人员获取数据里面内容的json语法写的不对 如$.code是获取响应内的code 但是响应如果用status表示,没有code那这样获取就会报错
其实就是测试人员的粗心所致，所以添加该功能，如果出现这种错误，会在报告上有详细信息显示

## 2.5 版本
修改 当条件为in时 如果jsonpath写错 也可以在报告上有详细信息显示

## 如果您觉得这个产品对您有用，您可以打赏下我，让我有理由继续下去，非常感谢。
![image-20210416143755979](https://woniumd.oss-cn-hangzhou.aliyuncs.com/test/zhangjing/20210416143756.png)
![image-20210416143919108](https://woniumd.oss-cn-hangzhou.aliyuncs.com/test/zhangjing/20210416143919.png)

 ## 当然你也可以 关注 加星 支持 非常感谢！！！

你也可以添加QQ：1576094876 进行技术探讨 需求更新 

