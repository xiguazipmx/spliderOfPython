# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    gender = scrapy.Field() #性别
    fans_count = scrapy.Field() #粉丝数
    statuses_count = scrapy.Field() #发的微博数
    follow_count = scrapy.Field() #关注数
    user_link = scrapy.Field() #个人主页连接
    avatar = scrapy.Field() #头像

class FansItem(scrapy.Item):
	"""粉丝列表"""
	user_id = scrapy.Field()
	fans = scrapy.Field()

class FollowsItem(scrapy.Item):
	"""关注列表"""
	user_id = scrapy.Field()
	follows = scrapy.Field()

class WeiBoItem(scrapy.Item):
	"""微博列表"""
	user_id = scrapy.Field()
	weibo_id = scrapy.Field()
	edit_date = scrapy.Field()
	text = scrapy.Field()
	text_length = scrapy.Field()
	source = scrapy.Field()