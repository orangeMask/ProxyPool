# -*- coding: utf-8 -*-
"""
@Author  : Jason
@Time    : 2021-7-21
@File    : python3.9
"""
import requests
import random
from datetime import datetime
import time
import re
from lxml import etree
from retrying import retry


# 抓取代理
class CrawlProxy(object):
    def crawl_run(self):
        proxies = self.parse_tool() + self.parse_ydl() + self.parse_kdl()
        return proxies

    @retry(stop_max_attempt_number=5)
    def request_page(self, url):
        # ua = random.choice(WINUA)
        ua = 'Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0'
        headers = {'User-Agent': ua}
        response = requests.get(url=url, headers=headers)
        return response

    def parse_ydl(self):
        proxies = []
        for p in (1, 10):
            url = f'http://www.ip3366.net/?stype=1&page={p}'
            response = self.request_page(url=url)
            tree = etree.HTML(response.text)
            trs = tree.xpath('.//tbody/tr')
            for items in trs:
                ip = items.xpath('./td[1]/text()')[0]
                port = items.xpath('./td[2]/text()')[0]
                proxy = ':'.join([ip, port])
                proxies.append(str(proxy))
        return proxies

    def parse_kdl(self):
        proxies = []
        for p in [1, 2]:
            for i in ['inha', 'intr']:
                url = f'https://www.kuaidaili.com/free/{i}/{p}/'
                response = self.request_page(url=url)
                tree = etree.HTML(response.text)
                uls = tree.xpath('.//table/tbody/tr')
                for items in uls:
                    ip = items.xpath('./td[@data-title="IP"]/text()')[0]
                    port = items.xpath('./td[@data-title="PORT"]/text()')[0]
                    proxy = ':'.join([ip, port])
                    proxies.append(str(proxy))
        return proxies

    def parse_tool(self):
        proxies = []
        for p in range(0, 100):
            url = f'https://toolbaba.cn/ip?p={p}'
            response = self.request_page(url=url)
            tree = etree.HTML(response.text)
            trs = tree.xpath('.//tbody/tr')
            for tr in trs:
                ip = tr.xpath('./td[1]/text()')[0]
                port = tr.xpath('./td[2]/text()')[0]
                ssl = tr.xpath('./td[3]/text()')[0]
                proxy = ':'.join([ip, port])
                proxies.append(str(proxy))
        return proxies
