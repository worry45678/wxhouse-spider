# -*- coding: utf-8 -*-
import scrapy

from autopjt.items import WXHouseItem


class WxhouseSpider(scrapy.Spider):
    name = 'wxhouse'
    allowed_domains = ['wxhouse.com']

    def start_requests(self):
        url = 'http://www.wxhouse.com:9097/wwzs/getzxlpxx.action'
        for i in range(1,200):
            yield scrapy.FormRequest(
                url = url,
                formdata = {'page.currentPageNo':str(i), 'page.pageSize':'15', 'page.totalPageCount':'199'}
            )
    def parse(self, response):
        item = WXHouseItem()
        item['name'] = response.xpath('//span[@style="color:#6A5ACD;font-size: 16"]/b/text()').extract()
        item['total'] = response.xpath('//span[@style="color:##AAAAAA"]/text()').extract()
        item['permit'] = response.xpath('//td[@style="background-color:#CCDDFF;height:82px;"]/text()').extract()
        item['link'] =  response.xpath('//a[@target="_blank"]/@href').extract()
        yield item
