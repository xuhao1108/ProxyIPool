import json
import random
from flask import Flask
from flask import request
from db.mongo_pool import MongoPool
from setting import AVAILABLE_IP_COUNT, FLASK_HOST, FLASK_PORT


class ProxyApi(object):
    """
    代理ip的web服务
    """

    def __init__(self):
        """
        初始化flask服务
        """
        # 创建flask服务
        self.app = Flask(__name__)
        # 创建数据库操作对象
        self.proxy_pool = MongoPool()

        @self.app.route('/random')
        def _random():
            """
            根据条件随意获取一个代理ip
            :return:
            """
            # 获取url中的请求参数
            protocol = request.args.get('protocol')
            nick_type = request.args.get('nick_type')
            domain = request.args.get('domain')
            nick_type = int(nick_type) if nick_type else None

            # 从数据库中取出数据
            proxy = self.proxy_pool.random(protocol=protocol, domain=domain, nick_type=nick_type,
                                           count=AVAILABLE_IP_COUNT)
            if proxy:
                # 判断是否有协议类型
                if protocol:
                    return "{}://{}:{}".format(protocol, proxy.ip, proxy.port)
                else:
                    return "{}:{}".format(proxy.ip, proxy.port)
            else:
                return ''

        @self.app.route('/proxies')
        def proxies():
            """
            根据条件获取若干个代理ip
            :return:
            """
            # 获取url中的请求参数
            protocol = request.args.get('protocol')
            nick_type = request.args.get('nick_type')
            domain = request.args.get('domain')
            count = request.args.get('count')
            nick_type = int(nick_type) if nick_type else None
            count = int(count) if count else AVAILABLE_IP_COUNT

            # 从数据库中取出数据
            proxies_list = self.proxy_pool.get_proxies(protocol=protocol, domain=domain, nick_type=nick_type,
                                                       count=count)
            # 用于存放若干个代理ip
            result = []
            # 依次将代理ip转化为字典格式并存入结果列表中
            for proxy in proxies_list:
                result.append(proxy.__dict__)
            # 将结果列表转化为字符串格式
            return json.dumps(result)

        @self.app.route('/disable_domain')
        def disable_domain():
            """
            更新此代理ip下的不可用域名列表
            """
            # 获取url中的请求参数
            ip = request.args.get('ip')
            domain = request.args.get('domain')

            # 判断传入参数是否为空
            if ip is None:
                return "请传入有效ip"
            if domain is None:
                return "请传入有效domain"

            # 更新此代理ip下的不可用域名列表
            self.proxy_pool.disable_domain(ip=ip, domain=domain)
            return "此代理ip不可用域名列表更新成功"

        @self.app.route('/headers')
        def headers():
            # 请求头
            with open('user-agent.txt', 'r', encoding='utf-8') as f:
                USER_AGENTS_LIST = f.readlines()
            # 去掉开头的"，末尾的"\n
            return str(random.choice(USER_AGENTS_LIST)[1:-2])

    def run(self):
        """
        启动flask服务
        :return:
        """
        self.app.run(host=FLASK_HOST, port=FLASK_PORT)

    @classmethod
    def start(cls):
        """
        开启web服务
        :return:
        """
        # 创建并运行web服务
        api = cls()
        api.run()


if __name__ == '__main__':
    ProxyApi.start()
