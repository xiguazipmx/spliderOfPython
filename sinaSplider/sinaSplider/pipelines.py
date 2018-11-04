# -*- coding: utf-8 -*-
import pymongo
from sinaSplider.items import FollowsItem,FansItem,UserItem,WeiBoItem
from scrapy.conf import settings

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinaspliderPipeline(object):

	def __init__(self):
		self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
		self.db = self.client[settings['MONGO_DB']]
		self.User = self.db['user']
		self.Fans = self.db['fans']
		self.Follows = self.db['follows']
		self.WeiBo = self.db['weibo']

	# def __init__(self, mongo_url, mongo_db):
	# 	self.mongo_url = mongo_url
	# 	self.mongo_db = mongo_db

	# @classmethod
	# def from_crawler(cls, crawler):
	# 	return cls(
	# 		mongo_url = crawler.settings.get('MONGO_URL'),
	# 		mongo_db = crawler.settings.get('MONGO_DATABASE')
	# 	)

	# def open_splider(self, splider):
	# 	self.client = pymongo.MongoClient(self.mongo_url)
	# 	self.db = self.client[self.mongo_db]
	# 	self.User = db['user']
	# 	self.Fans = db['fans']
	# 	self.Follows = db['follows']
	# 	self.WeiBo = db['weibo']

	# def close_splider(self, splider):
	# 	self.client.close()

	def process_item(self, item, splider):
		if isinstance(item, UserItem):
			try:
				self.User.insert(dict(item))
			except Exception as e:
				pass
		if isinstance(item, WeiBoItem):
			try:
				self.WeiBo.insert(dict(item))
			except Exception as e:
				pass
		if isinstance(item, FollowsItem):
			followsItems = dict(item)
			follows = followsItems.pop("follows")
			for i in range(len(follows)):
				followsItems[str(i+1)] = follows[i]
			try:
				self.Follows.insert(followsItems)
			except Exception as e:
				pass
		elif isinstance(item, FansItem):
			fansItems = dict(item)
			fans = fansItems.pop("fans")
			for i in range(len(fans)):
				fansItems[str(i+1)] = fans[i]
			try:
				self.Fans.insert(fansItems)
			except Exception as e:
				pass
		return item
