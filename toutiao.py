# -*- coding: utf-8 -*-

from urllib.parse import urlencode
from requests.exceptions import RequestException
import requests
import json
from bs4 import BeautifulSoup
import re
import os
from hashlib import md5

def get_page_index(offset,keyword):
    data = {
        "offset": offset,
        "format": 'json',
        "keyword": keyword,
        "autoload": 'true',
        "count": '20',
        "cur_tab": 1,
        "from": 'gallery',
    }
    url = 'https://www.toutiao.com/search_content/?'+urlencode(data)
    try:
        reponse = requests.get(url)
        if reponse.status_code == 200:
            return reponse.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None

def parse_page_index(html):
    print('--------------------')
    print(html)
    print('----------------------')
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detail(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        reponse = requests.get(url,headers = headers)
        if reponse.status_code == 200:
            return reponse.text
        return None
    except RequestException:
        print('请求详情页页出错',url)
        return None

def parse_page_detail(html,url):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    images_pattern = re.compile(r'gallery: JSON.parse\("(.*?)"\),',re.S)
    result = re.findall(images_pattern,html)
    data = result[0].replace('\\','')
    if result:
        sub_images = json.loads(data).get('sub_images')
        images = [item.get('url') for item in sub_images]
        for image in images:
            download_image(image,title)
        return {
            'title':title,
            'url':url,
            'images':images
        }

def download_image(url,title):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        reponse = requests.get(url,headers = headers)
        if reponse.status_code == 200:
            print('当前正在下载', url)
            save_image(reponse.content,title)
        return None
    except RequestException:
        print('请求图片出错',url)
        return None

def save_image(content,title):
    file_path = '{0}/{1}.{2}'.format(os.getcwd()+"\\play_time\\"+title,md5(content).hexdigest(),'jpg')
    if os.path.exists(os.getcwd()+"\\play_time\\"+title):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()
    else :
        os.makedirs(os.getcwd() + "\\play_time\\" + title)

def main():
    html = get_page_index(0,'漂亮小姐姐')
    for url in parse_page_index(html):
        if url:
            html = get_page_detail(url)
            if html:
                result = parse_page_detail(html,url)

if __name__ == '__main__':
    main()


