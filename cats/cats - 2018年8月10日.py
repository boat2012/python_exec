#-*- coding：utf-8 -*-

import time
import os
import sys
import traceback
from PIL import Image
import numpy as np
import time
import pytesseract

WAIT_TIME = 3
Crown = 3   #要多少颗皇冠
filepath = "C:\\Users\\boat1\\Documents\\Code\\Cats\\"
os.environ['TESSDATA_PREFIX'] = "C:/Program Files (x86)/Tesseract-OCR/"
os.environ['PATH'] += os.pathsep + "C:/Program Files (x86)/Tesseract-OCR/"
#llife=(814,114,954,179)
#lattack = (820,196,954,257)
rlife=(976,114,1150,182)
i_our_attack = 2658
#rattack=(969,196,1101,257)

def main():

    if len(sys.argv) < 2:
        # check the sites file
        Crown = 3  #一个箱子
    else:
        Crown = int(sys.argv[1])
        print(u"箱子数：",Crown,end=' ', flush=True)

    # sys.exit(1)
    os.chdir(filepath)

    start_time = time.time()

    print("开始时间：", time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    os.system('adb shell input tap 1390 957')  #快速
    time.sleep(WAIT_TIME)

    ic = 0 # 场次
    while ic < Crown*5:
        ic = ic+1
        print("\n第 %d 场 "%(ic), end='', flush=True)
        # print("第",ic,"场   ",end=' ')
        try:
            pull_screenshot()
            image = Image.open(filepath+"1.png")
        
            #i_our_attack = int(pytesseract.image_to_string(image.crop(lattack),lang="eng"))
            
            i_their_life = get_rect(image,rlife)
            print(i_their_life, end='', flush=True)
            while i_our_attack < i_their_life:
                print("jump", end=' ', flush=True)
                os.system('adb shell input tap 1840 980') #跳过
                #time.sleep(1.5)
                time.sleep(WAIT_TIME) #保险，多些时间
                pull_screenshot()
                image = Image.open(filepath+"1.png")

                #i_our_attack = pytesseract.image_to_string(image.crop(lattack),lang="eng")
                i_their_life = get_rect(image,rlife)
                print(i_their_life,end=' ', flush=True)
            click_confirm()     #点屏幕上任何一点，开始战斗
            time.sleep(2*WAIT_TIME)
            click_confirm()     #等待战斗结束后确认
            time.sleep(5*WAIT_TIME)
            # print ic,
            #if i<4:
            # print("快速战斗",end="")
            os.system('adb shell input tap 1390 957')  #快速
            time.sleep(WAIT_TIME)
        except Exception as e: 
            print('出现错误:',end="") # str(Exception)
            #print 'str(Exception):\t', str(Exception)
            #print 'str(e):\t\t', str(e)
            #print 'repr(e):\t', repr(e)
            #print 'e.message:\t', e.message
            #print 'traceback.print_exc():'; traceback.print_exc()
            #print 'traceback.format_exc():\n%s' % traceback.format_exc()
            os.system("move C:\\Users\\boat1\\Documents\\Code\\Cats\\1.png C:\\Users\\boat1\\Documents\\Code\\Cats\\%d.png 1>nul 2>nul" % ic)
            time.sleep(WAIT_TIME)  
                        
            os.system('adb shell input tap 1840 980') #跳过
            time.sleep(WAIT_TIME)
            #os.system('adb shell input tap 1390 957')  #快速
            ic = ic - 1
    print("结束时间：", time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    print("程序运行了：--- %s seconds ---" % (time.time() - start_time))

def pull_screenshot():
    os.system('adb shell screencap -p /sdcard/1.png')
    os.system('adb pull /sdcard/1.png . 2>nul')
    
def click_confirm():
    print("confirm", end=' ', flush=True)
    os.system('adb shell input tap 971 910') #中间点击确定 

#由于都是数字    
#对于识别成字母的 采用该表进行修正    
rep={'O':'0',    
    'I':'1','L':'1',    
    'Z':'2',    
    'S':'8'    
    };    

def  getverify1(text):          
    #识别对吗    
    # print text
    text = text.strip()    
    text = text.upper(); 
    for r in rep:    
        text = text.replace(r,rep[r])     
    #out.save(text+'.jpg')    
    #print text,type(text)
    #text = filter(str.isdigit, text.encode("gbk"))  # python2 
    text = list(filter(str.isdigit, text))
    # print text
    #return int(text)     # python2
    return int(''.join(text)) 
    
def get_rect(img,rect): #输入图片，坐标值，返回识别后的数值
    image = img.crop(rect)
    image = del_red(image)
    #以下二值化
    imgry = image.convert('L')

    #通过阈值来分割

    threshold = 230
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    #二值化
    out = imgry.point(table, '1')
    #out.show()
    i_their_life = pytesseract.image_to_string(out,config="-psm 7",lang="eng")
    # print i_their_life
    return getverify1(i_their_life)

def del_red(img): # 把有红色的部分删除，返回一个img
    width, height = img.size[:2]
    #print width,height
    px = np.array(img)
    #print "px:",px[0,0]
    i = 0 
    j = 0 
    red_found = False
    xpos = width
    while not red_found and j < height:
        while not red_found and i < width:
            #print px[j][i]
            # print i,width,i<width-1
            r,g,b,v = px[j][i]
            if r>200 and g<100 and b<100 :
                #print "found"
                if xpos > i :
                    xpos = i
            i = i + 1
        i = 0
        j = j + 1
        # print j
    # print red_found,"x pos:",xpos
    return img.crop((0,0,xpos,height))

if __name__ == '__main__':
    main()
