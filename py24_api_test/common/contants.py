import os
"""

该模块用来处理整个项目目录的路径
"""

# res = os.path.dirname(__file__)
# BASEDIR = os.path.dirname(res)

# 当前文件的绝对路径获取
# dir = os.path.abspath(__file__)
# 项目目录路径
BASEDIR = os.path.dirname(os.path.dirname(__file__))
# BASEDIR2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASEDIR)

# 配置文件目录路径
CONF_DIR = os.path.join(BASEDIR,'conf')

# 用例数据目录
DATA_DIR = os.path.join(BASEDIR,'data')

# 日志文件目录
LOG_DIR = os.path.join(BASEDIR,'log')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# 测试报告路径
REPORT_DIR = os.path.join(BASEDIR,'reports')

# 测试用例模块所在目录
CASE_DIR = os.path.join(BASEDIR,'testcases')





