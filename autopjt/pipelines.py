# -*- coding: utf-8 -*-
import codecs
import json
import re
from datetime import datetime

import pymysql

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AutopjtPipeline(object):
    def __init__(self, *args, **kwargs):
        self.file = codecs.open('./mydata2.json', 'wb', encoding='utf-8')
    
    def process_item(self, item, spider):
        #i = json.dumps(dict(item), ensure_ascii=False)
        #line = i + '/n'
        #self.file.write(line)
        for j in range(0, len(item['name'])):
            name = item['name'][j]
            price = item['price'][j]
            comnum = item['comnum'][j]
            link = item['link'][j]
            goods = {'name':name, 'price':price, 'comnum':comnum, 'link':link}
            i = json.dumps(goods, ensure_ascii=False)
            line = i + '\n'
            self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()

class AutopjtWXHousePipeline(object):
    def __init__(self, *args, **kwargs):
        self.file = codecs.open('./mydata3.csv', 'wb', encoding='utf-8')
    
    def process_item(self, item, spider):
        #i = json.dumps(dict(item), ensure_ascii=False)
        #line = i + '/n'
        #self.file.write(line)
        for j in range(0, len(item['name'])):
            id = item['link'][j].split('=')[1]
            name = item['name'][j]
            total, remain = re.findall(r'\d+', item['total'][j])
            permit = item['permit'][4 * j + 3].strip().replace('\r\n','')
            link = item['link'][j]
            #goods = {'name':name, 'total':total, 'remain':remain, 'permit':permit, 'link':link}
            #i = json.dumps(goods, ensure_ascii=False)
            line = f'{id},{name},{total},{remain},{permit},{link},\n'
            self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()

class AutopjtWXHouseSQLPipeline(object):
    def __init__(self, *args, **kwargs):
        self.conn = pymysql.connect(
            host='192.168.222.100',
            port=3306,
            db='ww',
            user='root',
            passwd='123456',
            charset='utf8',
            use_unicode=True)
        self.cur = self.conn.cursor()
    
    def process_item(self, item, spider):
        #i = json.dumps(dict(item), ensure_ascii=False)
        #line = i + '/n'
        #self.file.write(line)
        for j in range(0, len(item['name'])):
            id = item['link'][j].split('=')[1]
            #name = item['name'][j]
            total, remain = re.findall(r'\d+', item['total'][j]) # 正则查找文本中的两处数字
            #permit = item['permit'][4 * j + 3].strip().replace('\r\n','')
            #link = item['link'][j]
            date = datetime.now().strftime('%Y-%m-%d')
            #goods = {'name':name, 'total':total, 'remain':remain, 'permit':permit, 'link':link}
            #i = json.dumps(goods, ensure_ascii=False)
            #line = f'{id},{name},{total},{remain},{permit},{link},\n'
            #self.file.write(line)
            sql = f"""INSERT INTO wxhouse(house_id, remain, date) VALUES ({id}, {remain}, '{date}')"""
            self.cur.execute(sql)  # 执行sql语句 values作为第二个参数而不是直接在sql语句中这种写法可以防sql语句注入
            print(self.cur._last_executed)  # 打印 调试用
            self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close() # 关闭游标
        self.conn.close() # 关闭数据库
