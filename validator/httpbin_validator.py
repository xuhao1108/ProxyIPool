import time
import requests
import json
from utils.log import logger
from utils.headers import get_headers
from setting import TIME_OUT


def check_proxy(proxy):
    """
    检测代理ip可用性
    :param proxy:
    :return:
    """
    # 补全代理ip的url
    proxies = {
        'http': 'http://{}:{}'.format(proxy.ip, proxy.port),
        'https': 'https://{}:{}'.format(proxy.ip, proxy.port)
    }
    # 判断是否支持http类型
    http, http_nick_type, http_speed = _check_proxy_info(proxies)
    # 判断是否支持https类型
    https, https_nick_type, https_speed = _check_proxy_info(proxies, ishttp=False)
    if http and https:
        proxy.protocol = 2
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif https:
        proxy.protocol = 1
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    else:
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.speed = -1
    # 将代理ip保存到调试日志中
    logger.debug(proxy)
    return proxy


def _check_proxy_info(proxy, ishttp=True):
    """
    检测代理ip的访问速度及匿名程度
    :param proxy: 代理ip
    :param ishttp: 是否是http类型
    :return:
    """
    nick_type = -1
    speed = -1
    # 测试代理ip的url
    if ishttp:
        test_url = 'http://httpbin.org/get'
    else:
        test_url = 'https://httpbin.org/get'
    try:
        # 记录当前时间作为请求开始时间
        start_time = time.time()
        # 使用代理访问url
        response = requests.get(url=test_url, headers=get_headers(), timeout=TIME_OUT, proxies=proxy)
        # 判断是否访问成功
        if response.status_code == 200:
            # 计算访问成功的时间
            speed = round(time.time() - start_time, 2)
            # 将响应信息转化为字典格式
            response_dict = json.loads(response.text)
            headers = response_dict['headers']
            ip = response_dict['origin']
            # 从headers中取出Proxy-Connection，若无此键，则返回值为None
            proxy_connection = headers.get('Proxy-Connection')
            # 若有两个ip，则为透明代理
            if "," in ip:
                nick_type = 2
            # 若headers中包含Proxy-Connection，则为匿名代理
            elif proxy_connection:
                nick_type = 1
            # 否则就为高匿代理
            else:
                nick_type = 0
            return True, nick_type, speed
        else:
            return False, nick_type, speed
    except Exception as e:
        print(e)
        return False, nick_type, speed
