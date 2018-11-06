# -*- coding: utf-8 -*-
import pymongo
from sinaSplider.items import FollowsItem,FansItem,UserItem,WeiBoItem
from scrapy.conf import settings
import re, time

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

	def process_item(self, item, splider):
		if isinstance(item, UserItem):
			try:
				self.User.update({'user_id':item['user_id']},{'$set':dict(item)},True)
			except Exception as e:
				pass
		if isinstance(item, WeiBoItem):
			try:
				date = item['edit_date']
				#item['edit_date'] = item['edit_date'].strftime('%Y-%m-%d %H:%M')
				if re.match('刚刚', date):
					item['edit_date'] = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
				if re.match('\d+分钟前', date):
					minute = re.match('(\d+)', date).group(1)
					item['edit_date'] = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(minute) * 60))
				if re.match('\d+小时前', date):
					hour = re.match('(\d+)', date).group(1)
					item['edit_date'] = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(hour) * 60 * 60))
				if re.match('\d{2}-\d{2}', date):
					item['edit_date'] = time.strftime('%Y-', time.localtime()) + date + ' 00:00'
				if re.match('昨天.*', date):
					item['edit_date'] = re.match('昨天(.*)', date).group(1).strip()
					item['edit_date'] = time.strftime('%Y-%m-%d', time.localtime() - 24 * 60 * 60) + ' ' + date
				print('----------------------------------------------------------------------')
				print(item['edit_date'])
				print('----------------------------------------------------------------------')
				self.WeiBo.insert(dict(item))
			except Exception as e:
				pass
		if isinstance(item, FollowsItem):
			followsItems = dict(item)
			#方法用于删除数组的最后一个元素并返回删除的元素
			follows = followsItems.pop("follows")
			for i in range(len(follows)):
				followsItems[str(i+1)] = follows[i]
			try:
				self.Follows.update({'user_id':item['user_id']},{'$set':followsItems},True)
			except Exception as e:
				pass
		elif isinstance(item, FansItem):
			fansItems = dict(item)
			fans = fansItems.pop("fans")
			for i in range(len(fans)):
				fansItems[str(i+1)] = fans[i]
			try:
				self.Fans.update({'user_id':item['user_id']},{'$set':dict(item)},True)
			except Exception as e:
				pass
		return item
