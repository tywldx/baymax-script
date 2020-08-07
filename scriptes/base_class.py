from interface import base_class
from scriptes import env_router
from flask import g
import b_logger

class BaseClass(base_class.BaseClass):
    """
    基础类，用来定义对外调用，例如:
        redis,mq,api等，(mysql已经在底层进行封装)
    父类：base_class.BaseClass 中，是框架内预制的对外请求封装方法，包括API请求和Mysql请求
    对于其他类型的请求，需要对应的测试开发人员自行在该文件内进行封装。
    """
    def __init__(self):
        super(BaseClass, self).__init__()

# ######### 自定义第三方调用方法封装 BEGIN #######
#   以下代码内容 由用户需求自定义封装。
#   建议：1、将第三方的调用请求在这里进行封装，
#        2、对于业务代码的封装请自行开启package专门实现
#   请参考 _demo格式，将异常进行处理，使用户不再处理各种异常情况


    def _demo(self, param1):
        """
        todo: 自定义第三方调用demo
        """
        demo_router = env_router.EnvRouter()
        try:
            demo_option = demo_router.get_option_demo(g.env_name, param1)
            # 自定义第三方调用
            # demo_option
        except Exception as e:
            # 建议异常处理直接返回错误，
            # 不建议对同一类型的异常错误进行 “嵌套异常” 处理，会造成异常提示过多。
            raise Exception(e)


# ****** 自定义第三方调用方法封装 END ******** #

# ########### 以下代码内容 “慎改” ###########
#   以下内容为调用父类的方法，是代码框架预装的封装实现，
#   包括： API请求的 request
#       mysql请求的 execute\execute_count\execute_get_one 等。
#   具体实现请参考平台中的教程链接 
# ******************************** #

    def _get_host(self, application_name):
        return self.__get_host(application_name)

    def _request(self, opt):
        """
        请求参数 
        {\n
            url: 'url', # 请求地址, 
            method: 'get'、'post'  # 请求方法:
            headers: json # 请求header设置,json类型
            json: true,false,  # 返回结果是否需要json序列化
            body: json  # json类型数据格式，用在post请求下
        }
        """
        return self.__request(opt)

    def _execute_mysql(self, sql, db_name):
        """
        返回数据类型: SqlObj[]
        """
        return self.__execute(sql, db_name)
    
    def _execute_mysql_count(self, sql, db_name):
        """
        返回数据 (count, data)
        """
        return self.__execute_count(sql, db_name)
    
    def _execute_mysql_must_get_one(self, sql, db_name):
        """
        返回数据 SqlObj
        """
        return self.__execute_get_one(sql, db_name)
    
    