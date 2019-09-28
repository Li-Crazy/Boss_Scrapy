'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/7/28 16:06
@Software: PyCharm
@File    : models.py
'''
from datetime import datetime,timedelta

class ProxyModel(object):
    def __init__(self,data):
        self.ip = data['ip']
        self.port = data['port']
        self.expire_str = data['expire_time']
        self.blacked = False

        data_str, time_str = self.expire_str.split("")
        year, month, day = data_str.split("-")
        hour, minute, second = time_str.split(":")
        self.expire_time = datetime(year=int(year), month=int(month), day=int(day),
                             hour=int(hour), minute=int(minute),
                             second=int(second))

        #http/https://ip:port
        self.proxy = "https://{}:{}".format(self.ip,self.port)

    @property
    def is_expiring(self):
        now = datetime.now()
        if (self.expire_time - now) < timedelta(seconds=5):
            return True
        else:
            return False