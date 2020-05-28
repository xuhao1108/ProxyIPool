from spiders.run_spiders import RunSpiders
from proxy_test import ProxyTest
from proxy_api import ProxyApi
from multiprocessing import Process


def run():
    """
    启动各项服务
    :return:
    """
    # 将各个任务添加到进程列表中
    process_list = [Process(target=RunSpiders.start, name='run_spiders'),
                    Process(target=ProxyTest.start, name='proxy_test'),
                    Process(target=ProxyApi.start, name='proxy_api')]

    # 依次开启各个任务进程
    for process in process_list:
        # 设置进程守护
        process.daemon = True
        # 启动进程
        process.start()

    # 让主进程等待子进程执行完毕
    for process in process_list:
        process.join()


if __name__ == '__main__':
    run()
