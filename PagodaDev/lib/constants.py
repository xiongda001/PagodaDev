import os

# from lib.handleLogger import logger

# 获取项目根路径
# one_path = os.path.abspath(__file__)
# two_path = os.path.dirname(one_path)
# three_path = os.path.dirname(two_path)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取测试数据datas所在目录的绝对路径
DATAS_DIR = os.path.join(BASE_DIR, 'datas')

# 获取测试用例文件所在的绝对路径
TEST_DATAS_FILES_PATH = os.path.join(DATAS_DIR, 'TestCases.xlsx')

# 获取配置文件configs所在目录的路径
CONFIGS_DIR = os.path.join(BASE_DIR, 'configs')
CONFIGS_FILE_PATH = os.path.join(CONFIGS_DIR, 'testCase.conf')
print(f'配置文件所在路径：{CONFIGS_FILE_PATH}')

USER_ACCOUNTS_FILE_PATH = os.path.join(CONFIGS_DIR, 'user_accounts.configs')

# 日志文件所在目录路径
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
# LOGS_FILE_PATH = os.path.join(LOGS_DIR,'cases.log')

# 测试报告所在目录路径
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
# REPORTS_FILE_PATH = os.path.join(REPORTS_DIR,'test_report.html')

# 测试用例所在目录
CASES_DIR = os.path.join(BASE_DIR, 'cases')
# print(CASES_DIR)
