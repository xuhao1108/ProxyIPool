from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool
import importlib
import schedule
import time
from db.mongo_pool import MongoPool
from utils.log import logger
from validator.httpbin_validator import check_proxy
from setting import PROXIES_SPIDERS, SPIDER_INTERVAL


class RunSpiders(object):
    """
    启动各个爬虫
    """

    def __init__(self):
        """
        创建协程池及数据库操作对象
        """
        self.pool = Pool()
        self.proxy_pool = MongoPool()

    @staticmethod
    def _import_spider_instance():
        """
        动态导入各爬虫模块并创建爬虫对象
        :return:
        """
        # 存放爬虫对象
        instances = []
        # 依次导入各爬虫模块并创建爬虫对象
        for instance_path in PROXIES_SPIDERS:
            # 获取爬虫模块路径及爬虫类名称
            module_name, class_name = instance_path.rsplit('.', maxsplit=1)
            # 导入模块
            module = importlib.import_module(module_name)
            # 获取模块中的爬虫对象
            _class = getattr(module, class_name)
            # 创建爬虫对象，并加入爬虫列表中
            instances.append(_class())
        return instances

    def _run_spider(self, spider):
        """
        开启爬虫
        :param spider:
        :return:
        """
        try:
            # 获取代理ip数据
            for proxy in spider.get_proxies():
                if proxy is None:
                    continue
                # 检测此代理ip
                proxy = check_proxy(proxy)
                # 判断此代理ip是否有效
                if proxy.speed != -1:
                    # 将此代理ip保存到数据库中
                    self.proxy_pool.save(proxy)
        except Exception as e:
            logger.exception("爬虫{}出错，原因：{}".format(spider, e))

    def run(self):
        """
        将各个爬虫加入到协程池中，并启动
        :return:
        """
        # 导入爬虫模块，并创建对象
        spiders = self._import_spider_instance()
        # 将各个爬虫加入到协程池中
        for spider in spiders:
            # 异步非阻塞
            self.pool.apply_async(self._run_spider, args=(spider,))
        # 让主线程等待异步任务完成
        self.pool.join()

    @classmethod
    def start(cls):
        """
        开启爬虫服务
        :return:
        """
        # 创建并启动爬虫
        spiders = cls()
        spiders.run()

        # 设置定时启动爬虫
        schedule.every(SPIDER_INTERVAL).hours.do(spiders.run)
        while True:
            # 运行任务
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    RunSpiders.start()
