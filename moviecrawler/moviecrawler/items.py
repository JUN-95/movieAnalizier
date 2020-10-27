# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviecrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    form = scrapy.Field()
    movieName = scrapy.Field()
    score = scrapy.Field()
    image_urls = scrapy.Field()
    # images = scrapy.Field()
    image_paths = scrapy.Field()
    realContentLink = scrapy.Field()
    daoyan = scrapy.Field()
    bianju = scrapy.Field()
    zhuyan = scrapy.Field()
    type = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    time = scrapy.Field()
    duration = scrapy.Field()
    pass
