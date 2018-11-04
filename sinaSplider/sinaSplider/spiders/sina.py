import scrapy
from sinaSplider.items import UserItem,FansItem,FollowsItem,WeiBoItem
from scrapy.selector import Selector
import sys
import json
import requests
from scrapy.http import Request

class MySplider(scrapy.Spider):
	name = "sinaSplider"
	allowed_domains = ["m.weibo.cn"] #填写域名，表示允许爬虫访问的网站
	#start_urls = ["https://m.weibo.cn/profile/info?uid=2802828477"] #爬虫启动时获取的url列表。
	user_url = 'https://m.weibo.cn/profile/info?uid={uid}' #个人信息
	fans_url = 'https://m.weibo.cn/api/container/getSecond?containerid={containerid}_-_FANS&page={page}' #粉丝
	followers_url = 'https://m.weibo.cn/api/container/getSecond?containerid={containerid}_-_FOLLOWERS&page={page}' #关注
	weibo_url = 'https://m.weibo.cn/api/container/getIndex?containerid={containerid}_-_WEIBO_SECOND_PROFILE_WEIBO&page={page}'
	all_weibo = 'https://m.weibo.cn/statuses/extend?id={id}'

	start_users =[
		'6443964479'
	]

	#已经爬过的id
	finish_ID = set()
	#待爬的id
	wait_ID = set(start_users)

	def start_requests(self):
		while self.wait_ID.__len__():
			ID = self.wait_ID.pop()
			self.finish_ID.add(ID)#加入已爬列表
			#粉丝列表
			fans = []
			fansItems = FansItem()
			fansItems["user_id"] = ID
			fansItems["fans"] = fans
			#关注列表
			follows = []
			followsItems = FollowsItem()
			followsItems['user_id'] = ID
			followsItems['follows'] = follows
			#获取用户信息
			yield Request(url=self.user_url.format(uid=ID),
				meta={"fan_item":fansItems,"fan_result":fans,
					  "follow_item":followsItems,"follow_result":follows
					 },
				callback=self.user_request)


	#获取用户信息
	def user_request(self, response):
		fan_item = response.meta["fan_item"]
		follow_item = response.meta["follow_item"]
		fan_result = response.meta["fan_result"]
		follow_result = response.meta["follow_result"]

		user_json = json.loads(response.text)
		containerid = user_json.get('data').get('fans')
		weibo_containerid = user_json.get('data').get('more')
		user = user_json.get('data').get('user')
		fan_page = 1
		follow_page = 1
		weibo_page = 1

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
		yield Request(url=self.fans_url.format(containerid=containerid,page=int(fan_page)),
			meta={"item":fan_item,"result":fan_result,"page":fan_page,"containerid":containerid},
			callback=self.fans_request)
		yield Request(url=self.followers_url.format(containerid=containerid,page=int(follow_page)),
			meta={"item":follow_item,"result":follow_result,"page":follow_page,"containerid":containerid},
			callback=self.follow_request)

		weibo_containerid = weibo_containerid.replace("/p/","").replace("_-_WEIBO_SECOND_PROFILE_WEIBO","")
		weiboItem = WeiBoItem()
		weibo = []
		yield Request(url=self.weibo_url.format(containerid=weibo_containerid,page=int(weibo_page)),
			meta={"page":weibo_page},
			callback=self.weibo_request)

	#获取关注信息
	def follow_request(self, response):
		item = response.meta["item"]
		result = response.meta["result"]
		page = int(response.meta["page"])
		containerid = response.meta['containerid']
		follow_json = json.loads(response.text)

		if follow_json.get('ok') == 1:
			for follow in follow_json.get('data').get('cards'):
				follow_id = follow.get('user').get('id')
				result.append(follow_id)
				if follow_id not in self.finish_ID:
					self.wait_ID.add(follow_id)
					#粉丝列表
					# fans = []
					# fansItems = FansItem()
					# fansItems["user_id"] = follow_id
					# fansItems["fans"] = fans
					# #关注列表
					# follows = []
					# followsItems = FollowsItem()
					# followsItems['user_id'] = follow_id
					# followsItems['follows'] = follows
					#获取用户信息
					# yield Request(url=self.user_url.format(uid=follow_id),
					# 	meta={"fan_item":fansItems,"fan_result":fans,
					# 		  "follow_item":followsItems,"follow_result":follows
					# 		 },
					# 	callback=self.user_request)
			page = page + 1;
			yield Request(url=self.followers_url.format(containerid=containerid,page=int(page)),
				meta={"item":item,"result":result,"page":page,"containerid":containerid},
				callback=self.follow_request)
		else:
			yield item

	#获取粉丝信息
	def fans_request(self, response):
		item = response.meta["item"]
		result = response.meta["result"]
		page = int(response.meta["page"])
		containerid = response.meta['containerid']
		fans_json = json.loads(response.text)

		if fans_json.get('ok') == 1:
			for fan in fans_json.get('data').get('cards'):
				fan_id = fan.get('user').get('id')
				result.append(fan_id)
				if fan_id not in self.finish_ID:
					self.wait_ID.add(fan_id)
					#粉丝列表
					# fans = []
					# fansItems = FansItem()
					# fansItems["user_id"] = fan_id
					# fansItems["fans"] = fans
					# #关注列表
					# follows = []
					# followsItems = FollowsItem()
					# followsItems['user_id'] = fan_id
					# followsItems['follows'] = follows
					# #获取用户信息
					# yield Request(url=self.user_url.format(uid=fan_id),
					# 	meta={"fan_item":fansItems,"fan_result":fans,
					# 		  "follow_item":followsItems,"follow_result":follows
					# 		 },
					# 	callback=self.user_request)
			page = page + 1;
			print(page)
			yield Request(url=self.fans_url.format(containerid=containerid,page=int(page)),
				meta={"item":item,"result":result,"page":page,"containerid":containerid},
				callback=self.fans_request)
		else:
			yield item

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
					weiboItem['edit_date'] = w.get('mblog').get('edit_at')
					weiboItem['text'] = w.get('mblog').get('text')
					weiboItem['text_length'] = w.get('mblog').get('textLength')
					weiboItem['source'] = w.get('mblog').get('source')
					yield weiboItem
		else:
			page = page+1
			yield Request(url=self.weibo_url.format(containerid=weibo_containerid,page=int(weibo_page)),
			meta={"page":page},
			callback=self.weibo_request)