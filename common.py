# -*- coding: utf-8 -*-

################################################
# 一些常用的功能

# def yandex_mail(sub,content,to_list = mailto_list):
# sub 邮件标题
# content 邮件内容
# to_list: 要发往的邮件地址
# 使用: ct.yandex_mail(sub=(time.strftime("%m-%d %H:%M")+"报告"),content=outputText)
# 缺省的发往地址： mailto_list=["3223449@qq.com"]

#  海龟方法
#  输入 ： name 股票名称 
#  stockid 股票ID
#  pri:  如果没有满足海龟的买入卖出条件，是否打印
#  输出 一个三元组: 
#  buy or sell : 1 buy 0 don't do anything -1 sell
#  price: 当前价格（收盘）
#  atr: 波动幅度
#  haigui(name,stockid,pri=False): # pri为true 就不管有没有符合突破条件就都打印出来
#
#  获取一个股票的基金持有数据
#  scode = "300502"
#  sdate = "2020-12-31"
#  打印基金持股汇总，并返回一个基金持有数量的dataframe
#  def get_cyjj(scode,sdate): 

#  获取网页内容
"""
def get_page_context(url) -> tuple:
    用于爬取页面 爬取特定的网页
    :param url:要爬取的url
    :return: 返回二元组 爬取结果（success or error)，网页内容
    """

"""
Created on Sat Aug 01 17:28:29 2015
@author: lenovo
"""
import requests
from FundCrawler.FakeUAGetter import my_fake_ua
import json
import datetime
import pandas as pd
import sys
from email.mime.text import MIMEText
import smtplib
import baostock as bs
#import tushare as ts
import numpy as np
import logging
import ssl
"""
时间常数
"""


###############################################
mailto_list=["3223449@qq.com"]

#yandex_host = "smtp.yandex.com"
#my_mail="boat2019@yandex.com"
#my_mail="boat20200710@yandex.com"
#yandex_pass="3TFHBtSqTsiNSBc"
yandex_pass="jhfz1114"
my_mail = "boat_fj@163.com"
yandex_pass = "DOOATPXMIUMVFDRK"

############################################
GUPIN_FILE = "/home/pi/stock/daily/gupin.txt"   #股评文件
SHIBOR_FILE = "/home/pi/stock/daily/shibor.txt"  # shibor文件
HIGH_FILE = "/home/pi/stock/daily/high.txt"    # 新高文件
STOCKCHECK_FILE = "/home/pi/stock/daily/stockcheck.txt"   #邮件模板文件
TEMPLATE_FILE = "template.html"   #邮件模板文件

################################################
# sub 邮件标题
# content 邮件内容
# to_list: 要发往的邮件地址
# 使用: ct.yandex_mail(sub=(time.strftime("%m-%d %H:%M")+"报告"),content=outputText)
# 缺省的发往地址： mailto_list=["3223449@qq.com"]
def yandex_mail(sub,content,to_list = mailto_list):
    me = my_mail
    msg = MIMEText(content,_subtype='html',_charset='utf-8')    #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
    
        # s = smtplib.SMTP_SSL("smtp.yandex.com:465")
        s = smtplib.SMTP_SSL("smtp.163.com:465")
        s.ehlo()
        s.login(my_mail,yandex_pass)  #登陆服务器
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        s.close()
        return True
    except Exception as e:
        print(e)
        return False
        
###############################################

def CalcATR(data):
    TR_List=[]
    for i in range(1,21):
        TR=max(data['high'].iloc[-i]-data['low'].iloc[-i],abs(data['high'].iloc[-i]-data['close'].iloc[-i-1]),abs(data['close'].iloc[-i-1]-data['low'].iloc[-i]))
        TR_List.append(TR)
    ATR=np.array(TR_List).mean()
    return ATR     
    
def qujian(data,T):
    return max(data['high'].iloc[-T-1:-1]),min(data['low'].iloc[-int(T/2)-1:-1])

# 头寸规模单位 = 帐户的1% / 市场的绝对波动幅度
# 假设帐户
def CalcUnit(perValue,ATR):
    #print("perValue:",perValue,int((perValue*0.01/ATR)/100)*100)
    return int((perValue*0.01/ATR)/100)*100

#  return : 
#  buy or sell : 1 buy 0 don't do anything -1 sell
#  price: 当前价格（收盘）
#  atr: 波动幅度
def haigui(name,stockid,pri=False): # pri为true 就不管有没有符合突破条件就都打印出来

    # 帐户的价值，80万
    account_value = 800000 
    lg = bs.login()

    rs = bs.query_history_k_data_plus("sh.000001",
        "date,code,open,high,low,close,preclose,volume,amount,pctChg",
        start_date='2021-01-01', frequency="d")
    # rs = bs.query_history_k_data_plus("sh.000001",
    #     "date,code,open,high,low,close,preclose,lume,amount,pctChg",start_date='2021-01-01', frequency="d")
    # 打印结果集
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    #print(result)
    last_date=result.iloc[-1].date

    #logging.basicConfig(format="%(asctime)s -  %(message)s",filename="check_stock.log",level=logging.DEBUG)
    #df=ts.get_k_data(stockid)

    end_day=datetime.date(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day)  
    days=30*7/5  
    #考虑到周六日非交易  
    start_day=end_day-datetime.timedelta(days)  
    #print(start_day,end_day)
    start_day=start_day.strftime("%Y-%m-%d")  
    end_day=end_day.strftime("%Y-%m-%d")  
    # 获取股票数据
    rs = bs.query_history_k_data_plus(stockid,'date,high,low,close',start_date=start_day,end_date=end_day,frequency="d")
#     print('query_history_k_data_plus respond error_code:'+rs.error_code)
#     print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)
    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    df = pd.DataFrame(data_list, columns=rs.fields)
    df.high = df.high.astype(float)
    df.low = df.low.astype(float)
    df.close = df.close.astype(float)
    #print(df.iloc[-1].date)
    #print(last_date)

    if df.iloc[-1].date == last_date:
        high,low=qujian(df,20)
        price = df['close'].iloc[-1]
        #price = df['high'].iloc[-1]
        atr = CalcATR(df)
        unit = CalcUnit(account_value,atr)
        # logging.debug(last_date)
        if pri:
            #print(last_date)
            print(u"股票%s(%s)目前价位是%.2f，买入上限是%.2f，卖出下限是%.2f  " % (name,stockid,price,high,low))
            #print(u"波动幅度为：%.2f，买入的仓位为：%d股  " % (atr,unit))
            print(u"波动幅度为：%.2f，买入的仓位为：%d股  ,需要资金%d元" % (atr,unit,price*unit))
            #logging.debug(u"股票%s目前价位是%.2f，买入上限是%.2f，卖出下限是%.2f" % (stockid,price,high,low))
            #logging.debug(u"波动幅度为：%.2f，买入的仓位为：%d股" % (atr,unit))
        if price > high:
            print(u"股票%s(%s)目前价位是%.2f，可以买入，买入上限是%.2f，卖出下限是%.2f  " % (name,stockid,price,high,low))
            print(u"波动幅度为：%.2f，买入的仓位为：%d股  ,需要资金%d元" % (atr,unit,price*unit))
            # print(u"波动幅度为：%.2f，买入的仓位为：%d股  " % (atr,unit))
            #logging.debug(u"股票%s目前价位是%.2f，可以买入，买入上限是%.2f，卖出下限是%.2f" % (stockid,price,high,low))
            #logging.debug(u"波动幅度为：%.2f，买入的仓位为：%d股" % (atr,unit))
            return (1,price,atr)
        if price < low:
            print(u"股票%s(%s)目前价位是%.2f，应该卖出，买入上限是%.2f，卖出下限是%.2f  " % (name,stockid,price,high,low))
            print(u"波动幅度为：%.2f，买入的仓位为：%d股  ,需要资金%d元" % (atr,unit,price*unit))
            #logging.debug(u"股票%s目前价位是%.2f，应该卖出，买入上限是%.2f，卖出下限是%.2f" % (stockid,price,high,low))
            #logging.debug(u"波动幅度为：%.2f，买入的仓位为：%d股" % (atr,unit))
            return(-1,price,atr)
        return(0,price,atr)  


##  获取网页内容

def get_page_context(url) -> tuple:
    """
    用于爬取页面 爬取特定的网页
    :param url:要爬取的url
    :return: 返回二元组 爬取结果（success or error)，网页内容
    """
    header = {"User-Agent": my_fake_ua.random}
    import requests
    try:
        page = requests.get(url, headers=header)
        page.encoding = 'utf-8'
        result = ('success', page.text)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError):
        result = ('error', url)
    return result


###############################################


def get_cyjj(scode,sdate):  # 获取股票scode的基金持股信息，基于sdate发布的基金报告
    #返回df : "基金代码","基金名称","类型","持股总数","持股市值","占总股本比例","占流通市值比例"
    
    url = "http://data.eastmoney.com/dataapi/zlsj/detail?SHType=0&SHCode=&SCode=%s&ReportDate=%s" % (scode,sdate)
    result = get_page_context(url)
    fund_list = json.loads(result[1])
    df = pd.DataFrame(fund_list['data'])
    if(len(df)==0):
        print("截到%s,股票%s没有基金持有"% (sdate,scode))
        return None
    else:
        df = df[["f3","f4","f8","f9","f10","f11","f12"]].copy() # f3 基金代码 ， f4  基金名称, f8 类型, f9 持股总数，f10 持股市值， f11 占总股本比例，f12 占流通市值比例
        df[["f9","f10","f11","f12"]]=df[["f9","f10","f11","f12"]].apply(pd.to_numeric,errors='coerce')
        df.columns = ["基金代码","基金名称","类型","持股总数","持股市值","占总股本比例","占流通市值比例"]
        print("截到%s,股票%s共有%d家基金持有，持股总数为%.0f" % (sdate,scode,len(df),df["持股总数"].sum()))
        # print(len(df))
        return df    