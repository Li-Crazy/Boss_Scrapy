# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

import random
import requests
import json
from ..boss.models import ProxyModel
from twisted.internet.defer import DeferredLock

class UserAgentDownloadMiddlewares(object):
    USER_AGENTS = [
        'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo '
        'Browser 1.98.744; .NET CLR 3.5.30729)',
        'Mozilla/4.0 (compatible; MSIE 7.0; America Online Browser 1.1; '
        'Windows NT 5.1; (R1 1.5); .NET CLR 2.0.50727; InfoPath.1)',
        'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; '
        'Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
        'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ '
        '(KHTML, like Gecko)'
    ]
    def process_request(self,request,spider):
        user_agent = random.choice(self.USER_AGENTS)
        request.headers['User-Agent'] = user_agent

class IPProxyDownloadMiddleware(object):
    PROXY_URL = "代理服务API链接 "

    def __init__(self):
        super(IPProxyDownloadMiddleware,self).__init__()
        self.current_proxy = None
        self.lock = DeferredLock()

    def process_request(self,request,spider):
        if 'proxy' not in request.meta or self.current_proxy.is_expiring:
            #请求代理
            self.get_proxy()

        request.meta['proxy'] = self.current_proxy.proxy

    def process_response(self,request,response,spider):
        if response.status != 200 or "captcha" in response.url:
            if not self.current_proxy.blacked:
                self.current_proxy.blacked = True
            print("%s代理被加入到黑名单"%self.current_proxy.ip)
            self.update_proxy()
            #如果来到这里，说明这个请求被识别为爬虫，该请求相当于什么都没有获取
            #如果不返回request，则该request相当于没有获取到数据，就被废掉了
            #所以要重新返回request，将该请求重新加入到调度中，下次再发送
            return request
        #正常则返回response，不返回则response不会被传到爬虫那里去，得不到解析
        return response

    def update_proxy(self):
        self.lock.acquire()
        if not self.current_proxy or self.current_proxy.is_expiring or self.current_proxy.blacked:
            response = requests.get(self.PROXY_URL)
            text = response.text
            result = json.loads(text)
            print('重新获取了一个代理',text)
            if len(result['data'])>0:
                data = result['data'][0]
                proxy_model = ProxyModel(data)
                self.current_proxy = proxy_model
        self.lock.release()
