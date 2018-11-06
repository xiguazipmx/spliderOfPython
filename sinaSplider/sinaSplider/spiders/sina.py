import scrapy
from sinaSplider.items import UserItem,FansItem,FollowsItem,WeiBoItem
from scrapy.selector import Selector
import sys
import json
import requests
from scrapy.http import Request
from datetime import datetime

class MySplider(scrapy.Spider):
	name = "sinaSplider"
	allowed_domains = ["m.weibo.cn"] #填写域名，表示允许爬虫访问的网站
	user_url = 'https://m.weibo.cn/profile/info?uid={uid}' #个人信息
	fans_url = 'https://m.weibo.cn/api/container/getSecond?containerid={containerid}_-_FANS&page={page}' #粉丝
	follow_url = 'https://m.weibo.cn/api/container/getSecond?containerid={containerid}_-_FOLLOWERS&page={page}' #关注
	weibo_url = 'https://m.weibo.cn/api/container/getIndex?containerid={containerid}_-_WEIBO_SECOND_PROFILE_WEIBO&page={page}'
	all_weibo = 'https://m.weibo.cn/statuses/extend?id={id}'

	start_users =[
		'6443964479'
	]

	finish_ID = ()

	def start_requests(self):
		for uid in self.start_users:
			yield Request(url=self.user_url.format(uid=uid),callback=self.user_request)


	#获取用户信息
	def user_request(self, response):
		user_json = json.loads(response.text)
		containerid = user_json.get('data').get('fans')
		weibo_containerid = user_json.get('data').get('more')
		user = user_json.get('data').get('user')

		userItem = UserItem();
		userItem['user_id'] = user.get('id')
		userItem['user_name'] = user.get('screen_name')
		userItem['gender'] = user.get('gender')
		userItem['fans_count'] = user.get('followers_count')
		userItem['statuses_count'] = user.get('statuses_count')
		userItem['follow_count'] = user.get('follow_count')
		userItem['user_link'] = user.get('profile_url')
		userItem['avatar'] = user.get('avatar_hd')

		yield userItem

		containerid = containerid.replace("/p/second?containerid=","").replace("_-_FANS","")
		yield Request(url=self.fans_url.format(containerid=containerid,page=1),meta={"uid":user.get('id'),"page":1,"containerid":containerid},callback=self.fans_request)
		yield Request(url=self.follow_url.format(containerid=containerid,page=1),meta={"uid":user.get('id'),"page":1,"containerid":containerid},callback=self.follow_request)

		weibo_containerid = weibo_containerid.replace("/p/","").replace("_-_WEIBO_SECOND_PROFILE_WEIBO","")
		yield Request(url=self.weibo_url.format(containerid=weibo_containerid,page=1),meta={"uid":user.get('id'),"page":1,"containerid":weibo_containerid},callback=self.weibo_request)

	#获取关注信息
	def follow_request(self, response):
		page = int(response.meta["page"])
		uid = response.meta['uid']
		containerid = response.meta['containerid']
		follow_json = json.loads(response.text)

		if follow_json.get('ok') == 1:
			for follow in follow_json.get('data').get('cards'):
				follow_id = follow.get('user').get('id')
				yield Request(url=self.user_url.format(uid=follow_id),callback=self.user_request)
			follows = []
			for follow in follow_json.get('data').get('cards'):
				follows.append(follow.get('user').get('id'))
			followItems = FollowsItem()
			followItems['user_id'] = uid
			followItems['follows'] = follows
			yield followItems
		else:
			page = page+1
			yield Request(url=self.follow_url.format(containerid=containerid,page=page),meta={'uid':uid,'page':page,'containerid':containerid},callback=self.follow_request)

	#获取粉丝信息
	def fans_request(self, response):
		uid = response.meta['uid']
		page = int(response.meta["page"])
		containerid = response.meta['containerid']
		fans_json = json.loads(response.text)

		if fans_json.get('ok') == 1:
			for fan in fans_json.get('data').get('cards'):
				fan_id = fan.get('user').get('id')
				yield Request(url=self.user_url.format(uid=fan_id),callback=self.user_request)
			fans = []
			for fan in fans_json.get('data').get('cards'):
				fans.append(fan.get('user').get('id'))
			fanItems = FansItem()
			fanItems['user_id'] = uid
			fanItems['fans'] = fans
			yield fanItems
		else:
			page = page+1
			yield Request(url=self.fans_url.format(containerid=containerid,page=page),meta={'uid':uid,'page':page,'containerid':containerid},callback=self.fans_request)

	#获取微博信息
	def weibo_request(self, response):
		page = int(response.meta["page"])
		weibo_json = json.loads(response.text)

		if weibo_json.get('ok') == 1:
			weibo = weibo_json.get('data').get('cards')
			for w in weibo:
				if w.get('mblog'):
					weiboItem = WeiBoItem()
					weiboItem['user_id'] = w.get('mblog').get('user').get('id')
					weiboItem['weibo_id'] = w.get('mblog').get('id')
					weiboItem['edit_date'] = w.get('mblog').get('created_at')
					weiboItem['text'] = w.get('mblog').get('text')
					weiboItem['text_length'] = w.get('mblog').get('textLength')
					weiboItem['source'] = w.get('mblog').get('source')
					yield weiboItem
		else:
			page = page+1
			yield Request(url=self.weibo_url.format(containerid=weibo_containerid,page=int(weibo_page)),meta={"page":page},callback=self.weibo_request)

		def weibo_detail_request():
			pass