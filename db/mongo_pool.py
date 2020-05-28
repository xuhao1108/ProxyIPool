import pymongo
import random
from domain import Proxy
from setting import MONGO_URL
from utils.log import logger


class MongoPool(object):
    """
    操作mongodb数据库
    """

    def __init__(self):
        """
        连接mongodb
        """
        # 连接mongo
        self.client = pymongo.MongoClient(MONGO_URL)
        # 获取要操作的集合
        self.proxies = self.client['proxy_pool']['proxies']

    def __del__(self):
        """
        断开mongo
        :return:
        """
        # 断开mongo
        self.client.close()

    def insert(self, proxy):
        """
        插入新代理
        :param proxy: 新代理
        :return:
        """
        if proxy:
            # 将对象转换为字典
            proxy_dict = proxy.__dict__
            proxy_dict['_id'] = proxy.ip
            # 插入新代理
            self.proxies.insert_one(proxy_dict)
            logger.info("插入新代理IP:{}".format(proxy_dict))
        else:
            logger.error("没有传入要插入的proxy")

    def delete(self, proxy):
        """
        删除代理
        :param proxy: 要删除的代理
        :return:
        """
        if proxy:
            # 删除代理
            self.proxies.delete_one({'_id': proxy.ip})
            logger.info("代理IP删除成功:{}".format(proxy.__dict__))
        else:
            logger.error("没有传入要删除的proxy")

    def update(self, proxy):
        """
        更新代理
        :param proxy: 要更新的代理
        :return:
        """
        if proxy:
            self.proxies.update_one({'_id': proxy.ip}, {'$set': proxy.__dict__})
            logger.info("代理IP更新成功:{}".format(proxy.__dict__))
        else:
            logger.error("没有传入要更新的proxy")

    def find(self, conditions=None, count=0):
        """
        查询若干代理
        :param conditions: 查询条件
        :param count: 查询数目
        :return:
        """
        # 判断查询条件是否为空
        if conditions is None:
            conditions = {}
        # 查询
        cursor = self.proxies.find(conditions, limit=count).sort(
            [('sore', pymongo.DESCENDING), ('speed', pymongo.ASCENDING)]
        )
        # 存放查询结果
        find_result = []
        # 依次将查询结果转换为对象并添加到列表中
        for item in cursor:
            item.pop('_id')
            proxy = Proxy(**item)
            find_result.append(proxy)
        return find_result

    def save(self, proxy):
        """
        保存代理信息
        :param proxy: 要保存的代理
        :return:
        """
        # 判断数据库中是否存在此代理
        count = self.proxies.count_documents({'_id': proxy.ip})
        if count:
            # 更新此代理
            self.update(proxy)
        else:
            # 插入此代理
            self.insert(proxy)

    def get_proxies(self, protocol=None, nick_type=None, domain=None, count=0):
        """
        获取若干符合条件的代理
        :param protocol: 协议类型：2：支持http和https，1：支持https，0：支持http，-1：不可用
        :param nick_type: 匿名程度：2：透明代理，1：匿名代理，0：高匿代理，-1：不可用
        :param domain: 访问域名
        :param count: 数量
        :return:
        """
        # 存放查询条件
        conditions = {}

        if protocol is None:
            conditions['protocol'] = 2
        elif protocol.lower() == 'http':
            conditions['protocol'] = {'$in': [0, 2]}
        elif protocol.lower() == 'https':
            conditions['protocol'] = {'$in': [1, 2]}
        if nick_type is not None:
            conditions['nick_type'] = nick_type
        if domain:
            conditions['disable_domains'] = {'$nin': [domain]}
        return self.find(conditions, count=count)

    def random(self, protocol=None, nick_type=None, domain=None, count=0):
        """
        从若干符合条件的代理中获取一个
        :param protocol: 协议类型：2：支持http和https，1：支持https，0：支持http，-1：不可用
        :param nick_type: 匿名程度：2：透明代理，1：匿名代理，0：高匿代理，-1：不可用
        :param domain: 访问域名
        :param count: 数量
        :return:
        """
        # 获取若干代理
        proxy_list = self.get_proxies(protocol=protocol, domain=domain, nick_type=nick_type, count=count)
        # 随机取出一个代理
        return random.choice(proxy_list) if proxy_list else None

    def disable_domain(self, ip, domain):
        """
        设置此代理下的不可用域名
        :param ip:
        :param domain:
        :return:
        """
        # 判断数据库中是否存在此代理
        if self.proxies.count_documents({'_id': ip}):
            # 判断此代理是否存在该不可用域名
            if self.proxies.count_documents({'_id': ip, 'disable_domains': domain}):
                logger.error("此代理ip已存在该不可用域名：{},{}".format(ip, domain))
            else:
                # 更新此代理ip的不可用域名列表
                self.proxies.update_one({'_id': ip}, {'$push': {'disable_domains': domain}})
                logger.info("代理IP不可用域名更新成功:{},{}".format(ip, domain))
        else:
            logger.error("不存在此代理ip:{}".format(ip))
