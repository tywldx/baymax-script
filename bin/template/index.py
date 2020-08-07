from scriptes import base_class
import b_msg

class Instance(base_class.BaseClass):

    def demo(self,mobile):
        """
        info:
            title: demo
            detail: demo方法说明
            auth: 作者
            status: 发布
            save_time: 30 # 节省时间 min
            release_time: '2020/01/01 12:00:00'
        tags:
            - 标签1
        params:
            -  key: mobile
               label: 后台登录手机号
               schema:
                 commponent_type: input
                 value_type: string
        """
        # API 请求
        res = self._request({
          "url": '{}'.format(self._get_host('app_1'))
        })
        # 数据库链接
        datas = self._execute_mysql("select * from user where id = 1", "database_name")
        return b_msg.success(data=res)
