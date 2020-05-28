from spiders.base_spider import BaseSpider


class XiciSpider(BaseSpider):
    """
    https://www.xicidaili.com/
    """
    urls = ["http://www.xicidaili.com/nn/{}".format(i) for i in range(1, 10)]
    group_xpath = '//table[@id="ip_list"]/tr[position()>1]'
    detail_xpath = {'ip': './td[2]/text()', 'port': './td[3]/text()', 'area': './td[4]/a/text()'}


class Ip3366Spider(BaseSpider):
    """
    http://www.ip3366.net/free/?stype=1&page=1
    """
    urls = ["http://www.ip3366.net/free/?stype={}&page={}".format(i, j) for j in range(1, 10) for i in range(1, 2)]
    group_xpath = '//table[@class="table table-bordered table-striped"]/tbody/tr'
    detail_xpath = {'ip': './td[1]/text()', 'port': './td[2]/text()', 'area': './td[5]/text()'}


class IpHaiSpider(BaseSpider):
    """
    http://www.iphai.com/free/ng
    """
    urls = ["http://www.iphai.com/free/{}".format(i) for i in ["ng", "wg"]]
    group_xpath = '//table[@class="table table-bordered table-striped table-hover"]//tr[position()>1]'
    detail_xpath = {'ip': './td[1]/text()', 'port': './td[2]/text()', 'area': './td[5]/text()'}


class FreshSpider(BaseSpider):
    """
    https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1
    """
    urls = ["https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{}".format(i) for i in range(1, 7)]
    group_xpath = '//div[@class="hfeed site"]/table[position()=2]//tr[@class="cells"]'
    detail_xpath = {'ip': './td[2]/text()', 'port': './td[3]/text()', 'area': './td[5]/text()'}


class Ip66Spider(BaseSpider):
    """
    http://www.66ip.cn/1.html
    """
    urls = ["http://www.66ip.cn/{}.html".format(i) for i in range(1, 1000)]
    group_xpath = '//div[@class="containerbox boxindex"]//table//tr[position()>1]'
    detail_xpath = {'ip': './td[1]/text()', 'port': './td[2]/text()', 'area': './td[3]/text()'}
