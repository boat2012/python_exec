#-*-coding:utf-8-*-
from PIL import Image
import win32gui
import win32con
import win32api
import os
import threading
import urllib
import time
import sys
import json
import urllib.request
from PIL import Image,ImageDraw,ImageFont

#reload(sys)
#sys.setdefaultencoding('utf8')

icount = 0
time = 10
if time <= 0 :
    time = 60

urltemplate = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=%d&n=1&nc=1361089515117&FORM=HYLH1'
baImageUrlList = []
localFileName  = ''
localBMPFileName  = ''
imagedir = 'C:/Users/boat1/Pictures/Wallpapers/'
bmpdir = 'C:/Users/boat1/Pictures/Wallpapers/'
bmplist = []    

def main():
    #print("main:",icount)
    parserImageUrl()
    download_images()
    # image_convert_bmp()
    #set_wall_func()    

def parserImageUrl():

    for i in range(0, 9, 1):
        url = urltemplate % i
        # print(url)
        #content = urllib.urlopen(url).read()
        content = urllib.request.urlopen(url).read()
        decodedjson = json.loads(content)
        imageurl = decodedjson['images'][0]['url']
        imagedate = decodedjson["images"][0]['enddate']
        imagecopyright = decodedjson["images"][0]['copyright']
        baImageUrlList.append([imageurl,imagedate,imagecopyright])

def download_images():

    for url in baImageUrlList:
        imagename = imagedir + os.path.basename(url[1]) + ".jpg"
        # print(imagename)
        f = open(imagename, 'wb')
        conn = urllib.request.urlopen("http://cn.bing.com"+url[0])
        f.write(conn.read())
        f.close()
        ttfont = ImageFont.truetype("C:/Users/boat1/Pictures/Wallpapers/msyh.ttc",20)  #这里我之前使用Arial.ttf时不能打出中文，用华文细黑就可以
        im = Image.open(imagename)
        draw = ImageDraw.Draw(im)
        draw.text((10,10),url[2], fill=(255,255,255),font=ttfont)
        im.save(imagename,'jpeg')

def image_convert_bmp():
    imaglist = os.listdir(imagedir)
    for imagepath in imaglist:
        file_name = os.path.basename(imagepath)
        file_name_type = os.path.splitext(file_name)
        file_name = file_name_type[0]
        newpath = bmpdir + file_name + '.bmp'
        imagepath  = './images/' + imagepath

        bmplist.append(newpath)
        bmpImage = Image.open(imagepath)
        bmpImage.save(newpath, "BMP")
        
'''
def setWallpaper(imagepath):
    k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2") #2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,imagepath, 1+2)

#def set_wall_func():
    global icount
    print("func:",icount)
    bmplist = os.listdir(imagedir)
    list_size = len(bmplist)
    index = icount % list_size
    print("some:",list_size,index)
    filename = bmplist[index]
    icount += 1
    print(filename)
    setWallpaper(imagedir + filename)
    set_wall_timer()

#def set_wall_timer():
    timer = threading.Timer(10, set_wall_func)
    timer.start()
'''


if __name__ == '__main__':
    main()
 