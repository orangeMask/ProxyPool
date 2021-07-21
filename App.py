# -*- coding: utf-8 -*-
"""
@Author  : Jason
@Time    : 2021-7-21
@File    : python3.9
"""

from flask import Flask, g
from saveProxy import RedisClient

__all__ = ['app']

app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/random')
def get_proxy():
    """
    Get a Proxy
    :return: 随机代理
    """
    conn = get_conn()
    return conn.random()


@app.route('/count')
def get_counts():
    """
    Get the count of proxies
    :return: 代理池总量
    """
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    # app.run(host='xx.xxx.xx.xxx', port='xxxx')
    app.run(host='127.0.0.1', port='5000')
