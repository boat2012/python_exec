# 下载喜马拉雅上的音频文件

import requests
import re
import os
from bs4 import BeautifulSoup
import json
from common import legitimize

filepath = "c:/tmp"   # 下载下来的文件存放的目录
headers = {'User-Agent': 'Xiaomi'}

def _download(id,title,filepath):
    """  根据ID来下载音频，并存放在filepath目录下，名字为title.m4a
    """
    download_url = "https://www.ximalaya.com/revision/play/v1/audio?id=%s&ptype=1" % id
    print("start download {}".format(title))
    try :
        rt = requests.get(download_url, headers=headers)
        src = json.loads(rt.text)['data']['src']
        res = requests.get(src,headers=headers,stream=True)
        size = res.headers['content-length']
        filename = filepath+"/"+legitimize(title)+'.m4a'
        if os.path.exists(filename):
            if str(size) == str(os.path.getsize(filename)):
                print("Skipping {}: file already exists".format(filename))
                return
        with open(filename, 'wb') as f:
            for i in res.iter_content(chunk_size=1024**2):  # 边下载边存硬盘, chunk_size 可以自由调整为可以更好地适合您的用例的数字
                f.write(i)
                print("█",end="")
        print("done.")
    except requests.HTTPError as http_error:
        raise http_error

def request_with_retry(url,headers):
    retry_times = 3
    for i in range(retry_times):
        try:
            return requests.get(url=url,headers=headers)
        except requests.Timeout as e:
            raise "Time out"
        except requests.HTTPError as http_error:
            raise http_error

def main():
    for i in range(1,4):
        url = "https://www.ximalaya.com/shangye/20498134/p%d" % i
        print(url)
        r = request_with_retry(url=url, headers=headers)
        # regex = r"\{\"index\".*?\"trackId\":(.*?),"  ,,r'__INITIAL_STATE__ \s*=\s*({.*?})\s*;\s*$'
        regex = r'AlbumDetailTrackList":.*?(\[.*?\])\s*'
        # soup = BeautifulSoup(r.text,"html.parser")
        # script = soup.find('script', text=re.compile('INITIAL_STATE'))  #window.__INITIAL_STATE__ =
        tracks = re.search(regex,
                            r.text, flags=re.DOTALL | re.MULTILINE).group(1)

        tracks = json.loads(tracks)   # 一个json数组
        # tracks = data["store"]["AlbumDetailPage"]["albumInfo"]["tracksInfo"]["tracks"]

        # 以下是获取专辑总共的页数
        # regex='min=\"(\d)\" max=\"(\d)\"'
        # page=re.search(regex,r.text, flags=re.DOTALL | re.MULTILINE)
        # print(page.group(1),page.group(2))
        for track in tracks:
            # print("title:",track["title"],"  id:",track["trackId"]) 
            _download(track["trackId"],track["title"],filepath)
        print("page {} done.".format(i)) 

if __name__ == "__main__":
    main()