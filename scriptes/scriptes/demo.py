from scriptes import base_class
import b_msg

class Instance(base_class.BaseClass):

    def ready_clue(self,mobile):
        """
        info:
            title: 准备一条线索用户创建订单和诊断工具
            detail: 创建指定年级的正式/预备线索、分配到创建人名下、保存线索信息必填项
            auth: 李爽
            status: 发布
            release_time: '2020/07/09 12:00:00'
        tags:
            - 线索
        params:
            -  key: mobile
               label: 后台登录手机号
               schema:
                 commponent_type: input
                 value_type: string
        """
        # -------mysql请求-------
        # self._execute_mysql(sql语句, 数据库名称)
        # 返回结构体 {code:'', data:[]}
        # self._execute_mysql_must_get_one(sql语句, 数据库名称)
        # 直接返回执行结果，当返回结果为空时，抛出异常并结束本次请求
        # -------api请求-------
        # self._request({url: 'url地址', 'method': '请求方法：post/get','body': { json请求数据(post方法时有效) }, 'params': {json格式(get方法时有效), 'headers': {}}})
        # 返回序列化好的response,当返回结果错误时，直接抛出异常并结束本次请求
        res = self._request({
          "url": '{}'.format(self._get_host('app_1'))
        })
        # 数据库链接
        datas = self._execute_mysql("select * from user where ss id = 1", "k12_passport")
        print(datas)
        return b_msg.success(data=res)
