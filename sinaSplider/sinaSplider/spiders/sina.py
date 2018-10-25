import scrapy
from sinaSplider.items import SinaspliderItem
from scrapy.selector import Selector
import sys
import requests

class MySplider(scrapy.Spider):
	name = "sinaSplider"
	allowed_domains = ["weibo.cn"] #填写域名，表示允许爬虫访问的网站
	start_urls = ["https://m.weibo.cn/profile/info?uid=2802828477"] #爬虫启动时获取的url列表。

	def parse(self, response):
		select = Selector(response)
		print('----------------------------------')
		print(select)


