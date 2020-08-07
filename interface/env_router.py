class MysqlOption():
    def __init__(self):
        self.host = ""
        self.port = ""
        self.username = ""
        self.password = ""
        self.database = ""

class EnvRouter():
    def __init__(self):
        self.mysql_options = {}
        self.application_host={}
    
    def set_mysql_option(self, mysql_opt):
        self.mysql_options[mysql_opt['database']] = mysql_opt
    
    def set_application_host(self, app_name, host):
        self.application_host[app_name] = host

    def get_mysql_option(self, database):
        return self.mysql_options[database]
    
    def get_application_host(self, app_name):
        return self.application_host[app_name]