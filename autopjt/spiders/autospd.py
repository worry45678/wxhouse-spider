# -*- coding: utf-8 -*-
import scrapy
from autopjt.items import AutopjtItem
from scrapy.http import Request

class AutospdSpider(scrapy.Spider):
    name = 'autospd'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://category.dangdang.com/pg1-cp01.41.00.00.00.00-shbig.html']

    def parse(self, response):
        item = AutopjtItem()
        item['name'] = response.xpath("//a[@class='pic']/@title").extract()
        item['price'] = response.xpath("//span[@class='price_n']/text()").extract()
        item['link'] = response.xpath("//a[@class='pic']/@href").extract()
        item['comnum'] = response.xpath("//a[@name='itemlist-review']/text()").extract()
        yield item
        for i in range(1,6):
            url = f'http://category.dangdang.com/pg{i}-cp01.41.00.00.00.00-shbig.html'
            yield Request(url, callback=self.parse)