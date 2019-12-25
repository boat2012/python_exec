import requests,re,json,time
from lxml import etree

# 以下为雪球评论的网址
# https://xueqiu.com/query/v1/symbol/search/status?u=6004350486&uuid=1209767305081397248&count=10&comment=0&symbol=SH688018&hl=0&source=all&sort=time&page=2&q=&session_token=null&access_token=4bb9c131e3473cf1b507446aab849c958a12256b
url = "https://xueqiu.com/S/SH688018"

comment_url= 'https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol={symbol}&hl=0&source=user&sort=time&page={page}&_={real_time}'
session = requests.session()
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {'Host': 'xueqiu.com',
           'Referer': 'https://xueqiu.com/',
           'Origin':'https://xueqiu.com',
           'User-Agent': agent}
a = time.time()
real_time = str(a).replace('.', '')[0:-1]
print(a)
url = comment_url.format(symbol="SH688010", page=1, real_time=real_time)
url="https://xueqiu.com/query/v1/symbol/search/status?u=6004350486&uuid=1209767305081397248&count=10&comment=0&symbol=SH688018&hl=0&source=all&sort=time&page=2"
print(url)
s=session.get(url,headers=headers)
print(s.status_code)
print(s.text)
