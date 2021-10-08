from configparser import ConfigParser
from PagodaDev.lib.constants import CONFIGS_FILE_PATH, USER_ACCOUNTS_FILE_PATH


class HandleConfig:
    def __init__(self, file_name=None):
        """
        读取配置文件
        :param file_name:
        """
        self.file_name = file_name
        self.config = ConfigParser()
        self.config.read(self.file_name, encoding="utf-8")

    def get_value(self, section, option):
        """
        :param section:
        :param area_name:
        :param option:
        :return:
        """
        return self.config.get(section, option)

    def get_int(self, section, option):
        """
        :param section:
        :param option:
        :return:
        """
        return self.config.getint(section, option)

    def get_float(self, section, option):
        """

        :param section:
        :param option:
        :return:
        """
        return self.config.getfloat(section, option)

    def get_boolean(self, section, option):
        """

        :param section:
        :param option:
        :return:
        """
        return self.config.getboolean(section, option)

    def get_eval_data(self, section, option):
        """
        :param section:
        :param option:
        :return:
        """
        return eval(self.get_value(section, option))

    @staticmethod
    def write_config(datas, filename):
        """
        写数据到配置文件的方法
        :param data:
        :param filename:
        :return:
        """
        # 创建配置解析器对象
        config = ConfigParser()
        for key in datas:
            config[key] = datas[key]

        with open(filename, 'w') as file:
            config.write(file)


do_config = HandleConfig(CONFIGS_FILE_PATH)
do_config_2 = HandleConfig(USER_ACCOUNTS_FILE_PATH)

if __name__ == '__main__':
    do_config = HandleConfig(CONFIGS_FILE_PATH)
    do_config_2 = HandleConfig(USER_ACCOUNTS_FILE_PATH)

    # print(do_config.get_value('log', 'logger_level'))
    print(do_config.get_value('test-kt3', 'user'))

    # print(do_config_2.get_value('invest_user', 'mobilephone'))
    # print(do_config_2.get_value('invest_user', 'pwd'))
    # print(do_config.get_eval_data("excel","six_var"))
    # print(type(do_config.get_eval_data("excel", "six_var")))

    # datas = {'file path':{'cases_path':'test_cases.xlsx','log_path':'record_result.txt'},
    #          'msg':{'success_result':'Pass','fail_result':'Fail'}}
    # write_filename = "write_config2.ini"
    # HandleConfig.write_config(datas,write_filename)
