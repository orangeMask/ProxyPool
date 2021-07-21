REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = '*******'
REDIS_KEY = 'proxy'
DB = 0

TEST_URL = 'http://www.taobao.com/'
VALID_STATUS_CODES = [200, 301]

MIN_SCORE, MAX_SCORE = 8, 10
# 初始分数
INITIAL_SCORE = 10
# 最大批测试量
BATCH_TEST_SIZE = 10
# 代理池数量界限
POOL_UPPER_THRESHOLD = 1

# 检查周期
TESTER_CYCLE = 20
# 获取周期
GETTER_CYCLE = 300

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

API_HOST, API_PORT = '127.0.0.1', '5000'
