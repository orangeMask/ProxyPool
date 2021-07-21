# -*- coding: utf-8 -*-
"""
@Author  : Jason
@Time    : 2021-7-21
@File    : python3.9
"""
import redis
import re
from random import choice
from SETTING import *


class PoolEmptyError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池已经枯竭')


# 存储代理
class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=DB, decode_responses=True)

    # 添加代理，设置分数为最高
    def add(self, proxy, score=INITIAL_SCORE):
        """
        :param proxy: 代理
        :param score: 分数
        '''注意，此处将简单的参数传入改为字典形式'''
        :return: 添加结果
        """
        if not re.match(r'\d+\.\d+\.\d+\.\d+:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            # return self.db.rpush(REDIS_KEY, {'Proxy': Proxy, 'score': score})
            print('代理不存在，可加入', {proxy: score})
            # return self.db.zadd(REDIS_KEY, {Proxy: score})
            return self.db.zadd(REDIS_KEY, {proxy: score})

    # 随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
    def random(self):
        """
        :return: 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, MAX_SCORE)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    # 代理值减一分，小于最小值则删除
    def decrease(self, proxy):
        """
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    # 判断是否重复存在
    def exists(self, proxy):
        """
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) is None

    # 将代理设置为MAX_SCORE
    def max(self, proxy):
        """
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    # 获取数量
    def count(self):
        """
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY)

    # 获取全部代理
    def all(self):
        """
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    # 批量获取
    def batch(self, start, stop):
        """
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)
