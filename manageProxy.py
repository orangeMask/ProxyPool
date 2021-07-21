# -*- coding: utf-8 -*-
"""
@Author  : Jason
@Time    : 2021-7-21
@File    : python3.9
"""
import time
from multiprocessing import Process
from SETTING import *
# from Proxy import TestProxy, CrawlGet, App
from testProxy import Tester
from crawlGetter import Getter
from App import app


class Manage(object):
    def run_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        """
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def run_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        """
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def run_api(self):
        """
        开启API
        """
        # App.app.run()
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理池开始运行')

        if TESTER_ENABLED:
            tester_process = Process(target=self.run_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.run_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.run_api)
            api_process.start()
