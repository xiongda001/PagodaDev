from django.shortcuts import render

# Create your views here.
import pymysql
import random
from PagodaDev.lib.handleConfig import do_config


class HandleMySQL:
    """操作mysql数据库"""

    db_server = 'test'  # 全局切换数据库环境 测试环境=test，uat环境=uat
    db = {"test-kt3": "test", "uat-ks1": "uat"}

    def __init__(self) -> object:
        """
        连接mysql,创建连接通过游标去操作数据库
        :rtype: object
        """

        if self.db_server is self.db['test-kt3']:
            """TEST环境"""
            self.conn = pymysql.connect(host=do_config.get_value('test-kt3', 'host'),
                                        port=do_config.get_int('test-kt3', 'port'),  # 端口号必须为int
                                        user=do_config.get_value('test-kt3', 'user'),
                                        password=do_config.get_value('test-kt3', 'password'),
                                        db=do_config.get_value('test-kt3', 'db'),
                                        charset=do_config.get_value('test-kt3', 'charset'),
                                        cursorclass=pymysql.cursors.DictCursor)
            self.cursor = self.conn.cursor()

        elif self.db_server is self.db.get('uat-ks1'):
            """UAT环境"""
            self.conn = pymysql.connect(host=do_config.get_value('uat-ks1', 'host'),
                                        port=do_config.get_int('uat-ks1', 'port'),  # 端口号必须为int
                                        user=do_config.get_value('uat-ks1', 'user'),
                                        password=do_config.get_value('uat-ks1', 'password'),
                                        db=do_config.get_value('uat-ks1', 'db'),
                                        charset=do_config.get_value('uat-ks1', 'charset'),
                                        cursorclass=pymysql.cursors.DictCursor)
            self.cursor = self.conn.cursor()

    def run(self, sql, is_more=False):
        """
        运行sql语句
        :param sql:
        :param is_more:
        :return:
        """
        self.cursor.execute(sql)  # 执行sql语句
        self.conn.commit()  # 提交

        # 判断sql条件语句是否传入多个值
        if is_more:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def close(self):
        """
        关闭mysql
        :return:
        """
        self.cursor.close()
        self.conn.close()

    @staticmethod
    def create_mobile():
        """
        随机创建一个手机号
        :return:
        """
        start_mobile = ['130', '131', '132', '133', '134']
        start_num = random.choice(start_mobile)  # 从start_mobile随机获取一个值
        end_num = ''.join(random.sample('0123456789', 8))  # 从0123456789数字中随机抽取8位数

        return start_num + end_num

    def is_existed_mobile(self, mobile):
        """
        判断给定的手机号是否在数据库中存在
        :param self:
        :param mobile:11位手机号组成的字符串
        :return:True or False
        """
        sql = "select `identity` from member where `identity` = %s;"
        if self.run(sql):  # 如果手机号已存在返回True，否则返回False
            return True
        else:
            return False

    def create_not_existed_mobile(self):
        """
        获取未注册的手机号
        :param self:
        :return:
        """
        while True:
            one_mobile = self.create_mobile()  # 把新建的手机号赋值给one_mobile
            # 判断one_mobile是否在数据库中存在
            if not self.is_existed_mobile(one_mobile):
                break
        return one_mobile

    def get_existed_mobile(self, sql_1=None):
        one_mobile = self.run(sql_1)
        return one_mobile["MobilePhone"]  # 从返回的字典里获取手机号的值


# if __name__ == '__main__':
#     # 查询会员权益
#     # sql1 = "select * from member_equity where equityCode = '2075';"
#
#     # 查询试用会员付费会员的价格
#     sql1 = "select price from pay_member_type where shelvesStatus='U' and typeCode = 1;"
#
#     # 查询付费会员类型
#     sql2 = 'select * from pay_member_type ' \
#            'where typeName like "心享会员年卡%" and identifyCode = 1 and shelvesStatus = "U";'
#
#     # sql6 = 'insert into dev_info(ID,var_str,var_int,online,dev_sn,var_float,var_double) ' \
#     #        'values(%s,%s,%s,%s,%s,%s,%s)'
#
#     # 请求入口
#     do_mysql = HandleMySQL()
#     print(do_mysql.run(sql1, is_more=False))


def query_member_price(request):
    # 参数化
    do_mysql = HandleMySQL()
    # 查询试用会员付费会员的价格

    result = 100
    if request.method == 'GET':
        if request.GET.get('test') == 'env':
            if 'select_payMember_type' == '1':
                sql = "select price from pay_member_type where shelvesStatus='U' and typeCode = 1 limit 1;"
                result_dict = do_mysql.run(sql, is_more=False)
                # print(type(result_dict))
                result = result_dict.get('price')
                print(f'141行代码：{result}')
                return render(request, 'miniTool/index.html', {'result': result})

            elif 'select_payMember_type' == '2':
                sql = "select price from pay_member_type where shelvesStatus='U' and typeCode = 2 limit 1;"
                result_dict = do_mysql.run(sql, is_more=False)
                # print(type(result_dict))
                result = result_dict.get('price')
                return render(request, 'miniTool/index.html', {'result': result})

    return render(request, 'miniTool/index.html', {'result': result})

