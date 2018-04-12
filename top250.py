import requests
from bs4 import BeautifulSoup
import time
import random
import pymongo
# 创建数据库
client = pymongo.MongoClient('localhost',27017)
doubantop250 = client['doubantop250']
detail = doubantop250['detail']

# 设置header
header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Connection': 'keep - alive'
        }
# proxy_list=[
#     'http://39.134.10.4:8080',
#     'http://120.92.118.64:10010',
#     'http://14.118.253.200:6123'
# ]

# proxy_ip=random.choice(proxy_list)
# proxies ={'http:',proxy_ip}

movie_list = []
def get_pages_link():
    # https://movie.douban.com/top250?start=25
    for item in range(0,250,25):
        url = "https://movie.douban.com/top250?start={}".format(item)
        web_data = requests.get(url,headers=header)
        time.sleep(2)
        soup = BeautifulSoup(web_data.text,'lxml')
        for movie in soup.select('#wrapper li'):
            href = movie.select('.hd > a')[0]['href']
            name = movie.select('.hd > a > span')[0].text
            # bd = movie.select('.bd > p')[0].text.strip()
            star = movie.select('.rating_num')[0].text
            people = movie.select('.star > span')[3].text
            try:
                quote = movie.select('.inq')[0].text
            except :
                print("没有quote哦")
                quote = None
            data = {
                'url':href,
                # '背景/明星':bd,
                '评价人数':people,
                '片名':name,
                '评分':star,
                '名言':quote
            }
            # 将数据插入数据库
            detail.insert_one(data)
            print(data)
        print('\n'+' - '*50+'\n')


if __name__ =='__main__':
    get_pages_link()
