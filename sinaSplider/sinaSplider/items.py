# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaspliderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    gender = scrapy.Field() #性别
    followers_count = scrapy.Field() #粉丝数
    statuses_count = scrapy.Field() #发的微博数
    follow_count = scrapy.Field() #关注数
    user_link = scrapy.Field() #个人主页连接