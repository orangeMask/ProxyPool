# -*- coding: utf-8 -*-
"""
@Author  : Jason
@Time    : 2021-7-21
@File    : python3.9
"""
from manageProxy import Manage


def main():
    try:
        m = Manage()
        m.run()
    except:
        main()


if __name__ == '__main__':
    main()
