import logging

# 日志等级
LOG_LEVEL = logging.INFO
# 日志时间格式
LOG_TIME = '%Y-%m-%d %H:%M:%S'
# 日志文件名格式
LOG_FILENAME = 'log.log'
# 日志格式
LOG_FORMAT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'

# mongo数据库连接参数
MONGO_URL = 'mongodb://127.0.0.1:27017/'
# 连接超时时长
TIME_OUT = 10
# flask_api的host
FLASK_HOST = '0.0.0.0'
# flask_api的port
FLASK_PORT = 8888

# 对抓取到的ip进行评分，默认值50,最大值50
# 每检查一次,若请求失败,则-1分
# 若评分为0,则从数据库中删除此ip
# 默认值
DEFAULT_SCORE = 50

# 配置爬虫列表
PROXIES_SPIDERS = [
    'spiders.proxy_spiders.XiciSpider',
    'spiders.proxy_spiders.Ip3366Spider',
    'spiders.proxy_spiders.IpHaiSpider',
    'spiders.proxy_spiders.FreshSpider',
    'spiders.proxy_spiders.Ip66Spider'
]

# 爬虫抓取时间间隔，单位：小时
SPIDER_INTERVAL = 2
# 测试代理ip时间间隔，单位：小时
TEST_INTERVAL = 2

# 测试代理ip异步个数
TEST_ANSYC_COUNT = 10

# 每次随机获取的代理ip个数
AVAILABLE_IP_COUNT = 20
