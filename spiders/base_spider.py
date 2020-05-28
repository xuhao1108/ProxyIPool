import requests
from lxml import etree
from utils.headers import get_headers
from utils.log import logger
from domain import Proxy


class BaseSpider(object):
    """
    基础爬虫类
    """
    # 代理ip的url网址
    ulrs = []
    # 分组的xpath
    group_xpath = ''
    # 获取具体信息的xpath
    detail_xpath = {}

    def __init__(self, urls=[], group_xpath='', detail_xpath={}):
        """
        初始化urls和xpath
        :param urls:
        :param group_xpath:
        :param detail_xpath:
        """
        # 判断数据是否为空
        if urls:
            self.urls = urls
        if group_xpath:
            self.group_xpath = group_xpath
        if detail_xpath:
            self.detail_xpath = detail_xpath

    @staticmethod
    def get_page_from_url(url):
        """
        从url中获取到网页数据
        :param url:
        :return:
        """
        # 获取网页数据
        response = requests.get(url, headers=get_headers())
        if response.status_code != 200:
            logger.error("爬取：{}出错！状态码：{}".format(url, response.status_code))
        else:
            return response.content

    def get_proxies_from_page(self, page):
        """
        从网页数据中提取具体信息
        :param page:
        :return:
        """
        # 解析网页数据
        element = etree.HTML(page)
        # 获取分组数据
        group = element.xpath(self.group_xpath)
        # 遍历分组数据，依次提取出具体信息
        for detail in group:
            # 获取具体信息
            ip = self.get_first(detail.xpath(self.detail_xpath['ip']))
            port = self.get_first(detail.xpath(self.detail_xpath['port']))
            area = self.get_first(detail.xpath(self.detail_xpath['area']))
            # 创建代理对象
            proxy = Proxy(ip=ip, port=port, area=area)
            # 返回代理对象
            logger.info(proxy)
            yield proxy

    @staticmethod
    def get_first(data):
        """
        获取xpath提取结果中的第一条
        :param data:
        :return:
        """
        return data[0].strip() if len(data) != 0 else ''

    def get_proxies(self):
        """
        遍历url，获取各代理ip的具体信息
        :return:
        """        # 遍历url，获取各代理ip的具体信息
        for url in self.urls:
            # 获取网页数据
            page = self.get_page_from_url(url)
            if page:
                # 获取代理ip的信息，并转换为对象
                proxy = self.get_proxies_from_page(page)
                logger.info("爬取{}已完成！".format(url))
                yield from proxy
