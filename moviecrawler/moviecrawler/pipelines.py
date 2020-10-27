# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib.parse import urlparse

import scrapy
from scrapy import Request
from scrapy.exceptions import DropItem

from moviecrawler.items import MoviecrawlerItem


class MoviecrawlerPipeline(object):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def process_item(self, item, spider):
        for m, i in zip(item["movieName"], item["image_urls"]):
            yield Request(i, meta={"mn": "movieName"})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

    # def file_path(self, request, response=None, info=None):
    #     item = MoviecrawlerItem()
    #     mn = request.meta["mn"]
    #     item["image_paths"] = mn + ".jpg"
    #     return item


import pymysql

# pipeline连接mysql数据库
class MysqlPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='123456', db='movie', charset='utf8')

        self.cursor = self.conn.cursor()
        print("successfull connected !!!")
    def process_item(self, item, spider):
        # print("==========="+type(item['zhuyan']))
        insert_sql = """
        insert into movie2(movieName,score,daoyan,bianju,zhuyan,type,country,language,time,duration) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        values = (
        item['movieName'],item['score'],item['daoyan'], item['bianju'], item['zhuyan'], item['type'], item['country'],
        item['language'], item['time'], item['duration'])
        self.cursor.execute(insert_sql, values)
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
