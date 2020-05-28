from setting import DEFAULT_SCORE


class Proxy(object):
    """
    代理ip数据模型
    """

    def __init__(self, ip=None, port=None, protocol=-1, nick_type=-1, speed=-1, area=None, score=DEFAULT_SCORE,
                 disable_domains=None):
        """
        初始化代理ip信息
        :param ip: 地址
        :param port: 端口
        :param protocol: 支持的协议类型：2：支持http和https，1：支持https，0：支持http，-1：不可用
        :param nick_type: 匿名程度：2：透明代理，1：匿名代理，0：高匿代理，-1：不可用
        :param speed: 响应速度
        :param area: 所在地
        :param score: 评分
        :param disable_domains: 不可用域名列表
        """
        # 代理ip的地址
        self.ip = ip
        # 代理ip的端口
        self.port = port
        # 代理ip支持的协议类型：2：支持http和https，1：支持https，0：支持http，-1：不可用
        self.protocol = protocol
        # 代理ip的匿名程度：2：透明代理，1：匿名代理，0：高匿代理，-1：不可用
        self.nick_type = nick_type
        # 代理ip的响应速度
        self.speed = speed
        # 代理ip的所在地
        self.area = area
        # 代理ip的评分
        self.score = score
        # 代理ip的不可用域名列表
        if disable_domains is None:
            self.disable_domains = []
        else:
            self.disable_domains = disable_domains

    def __str__(self):
        """
        返回代理ip信息
        :return:
        """
        return str(self.__dict__)
