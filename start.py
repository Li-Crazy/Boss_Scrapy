'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/7/25 17:26
@Software: PyCharm
@File    : start.py
'''
from scrapy import cmdline

cmdline.execute("scrapy crawl zhipin".split())