# ###########  说明 ########## #
#   这是接入方处理环境的入口文件，需要将环境信息在这里进行标准化，方便 base_class 类中，对环境信息进行获取。
#   需要注意的是必须保留三个方法： get_env_list、get_mysql_option、get_application_host
#   对于新扩展的环境信息配置请单独编写 get方法，并在base_class中调用
#   建议的配置获取方案：
# ############################ #

class EnvRouter():
# ###################  自定义代码区域 ################### #
    def __init__(self):
        """
        获取配置对象，
        数据库配置结构标准Dict：
        todo: 开发人员需要根据组织下测试环境的各自情况，将配置进行完善。
        """
        pass
    
    def get_env_list(self):
        """
        todo: 获取所有的环境名称，开发人员需要根据组织下的测试环境进行完善。
        """
        return ['env1', 'env2']

    def get_option_demo(self, env_name, param1):
        """
        获取配置的 demo代码
        """
        if True:
            return '获取配置内容'
        else:
            raise Exception("【{}】环境的XX【{}】demo配置不存在".format(env_name, param1))

# ###################  自定义代码区域 END ################### #

# ###################  以下是固定方法，不允许删除，因方法已经在基础调用中被引用 ################### #
    def get_mysql_option(self, env_name, database_name):
        """
        通过环境名称env_name,获取该环境下的 mysql_option 配置
        """
        print(env_name, database_name)
        if True:
            return True, {
                "host": "0.0.0.0",
                "port": "3301",
                "user": "user",
                "passwd": "pwd"
            }
        else:
            return False, "【{}】环境的数据库【{}】配置不存在".format(env_name, database_name)
    
    def get_application_host(self, env_name, application_name):
        """
        通过环境名称env_name,获取该环境下的 application_host_options 配置
        """
        if True:
            return 'http://www.baidu.com'
        else:
            raise Exception("【{}】环境的应用【{}】域名不存在".format(env_name, application_name))
    