from gevent import monkey

monkey.patch_all()

import schedule
import time
from gevent.pool import Pool
from multiprocessing import Queue
from db.mongo_pool import MongoPool
from validator.httpbin_validator import check_proxy
from setting import DEFAULT_SCORE, TEST_ANSYC_COUNT, TEST_INTERVAL


class ProxyTest(object):
    """
    测试代理ip可用性
    """

    def __init__(self):
        """
        初始化进程池、队列及数据库操作对象
        """
        self.pool = Pool()
        self.queue = Queue()
        self.mongo_pool = MongoPool()

    def _test_proxies(self):
        """
        测试代理ip可用性，并更新到数据库
        :return:
        """
        # 从队列中取出一个代理ip
        proxy = self.queue.get()
        try:
            # 检测代理ip
            proxy = check_proxy(proxy)
            # 判断此代理ip此次是否有效，若有效则恢复为默认分值，否则分值减1
            if proxy.speed == -1:
                proxy.score -= 1
                # 若评分为0，则表示此代理ip不可用，则从数据库中删除此代理ip
                if proxy.score == 0:
                    self.mongo_pool.delete(proxy)
                else:
                    # 更新此代理ip
                    self.mongo_pool.update(proxy)
            else:
                # 此代理ip恢复为默认分值
                proxy.score = DEFAULT_SCORE
                # 更新此代理ip
                self.mongo_pool.update(proxy)
        except Exception as e:
            print(e)

    def _test_callback(self, source):
        """
        检测代理ip(_test_proxies)的回调函数
        :param source: 回调函数所需参数
        :return:
        """
        # 使其死循环，不断检测代理ip
        self.pool.apply_async(self._test_proxies, callback=self._test_callback)

    def run(self):
        """
        启动代理ip的检测
        :return:
        """
        # 从数据库中获取所有代理ip
        proxies = self.mongo_pool.find()
        # 判断是否有代理ip
        if proxies is None or len(proxies) == 0:
            print("代理ip池为空")
            return

        # 依次将代理ip添加到队列中
        for proxy in proxies:
            self.queue.put(proxy)

        # 开启若干进程，用于检测代理ip
        for test in range(TEST_ANSYC_COUNT):
            # 异步非阻塞
            self.pool.apply_async(self._test_proxies, callback=self._test_callback)

        # 让主线程等待异步任务完成
        self.pool.join()

    @classmethod
    def start(cls):
        """
        开启检测代理ip服务
        :return:
        """
        # 创建并启动检测
        test = cls()
        test.run()

        # 定时启动检测
        schedule.every(TEST_INTERVAL).hours.do(test.run)
        while True:
            # 运行任务
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    ProxyTest.start()
