# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_demo.boss.boss.items import BossItem


class ZhipingSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c100010000/?query=python&page=1&ka=page-1']

    rules = (
        #匹配职位列表页的规则
        Rule(LinkExtractor(allow=r'.+\?query=python&page=\d'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'.+job_detail/\d+.html'), callback='parse_job', follow=False),
    )

    def parse_job(self, response):
        # item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
        name = response.xpath("//h1[@class='name']/text()").get().strip()
        salary = response.xpath("//h1[@class='name']/span/text()").get().strip()
        job_info = response.xpath("//div[@class='job-primary']/div[@class='info-primary']/p//text()").getall()
        city = job_info[0]
        work_years = job_info[1]
        education = job_info[2]
        company = response.xpath("//div[@class='job-company']//a/text()").get()
        item = BossItem(name=name,salary=salary,city=city,work_years=work_years,education=education,company=company)
        yield item