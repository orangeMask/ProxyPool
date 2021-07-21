# -*- coding: utf-8 -*-
"""
@Author  : Jason
@Time    : 2021-7-21
@File    : python3.9
"""

from saveProxy import RedisClient
from crawlProxy import CrawlProxy

# 代理池数量界限
POOL_UPPER_THRESHOLD = 500


class Getter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = CrawlProxy()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('获取器开始执行')
        # if not self.is_over_threshold():
        proxies = self.crawler.crawl_run()
        # print(proxies)
        # print(len(proxies))
        for proxy in proxies:
            self.redis.add(proxy)
            # print(Proxy)
