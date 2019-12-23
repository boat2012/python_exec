# 将东方财富基金排名的网站上相关的数据抓取下来，存入本地的excel文件

from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.action_chains import ActionChains

# 输入：  url : 获取基金的网页  filename:要存入的csv文件名
def getjj(url,filename):
    driver = webdriver.Ie()
    driver.get(url)
    # print("1-->",end=" ")
    while True:
        try:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            table = soup.find('table',{"id":"dbtable"})
            target = driver.find_element_by_xpath("//label[text()='下一页']")
            pvalue = target.get_attribute("value")
            df = pd.read_html(str(table))
            print("#",end="")
            df[0].to_csv(filename,mode='a',header=False) 
            if(target.get_attribute("class")=="end"):
                print("end")
                break
            js = 'var xpath ="//label[text()=\'下一页\']";var matchingElement = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();'
            driver.execute_script(js)
            time.sleep(2)
            target = driver.find_element_by_xpath("//label[text()='下一页']")
            nvalue = target.get_attribute("value")
            print(pvalue,end="")
            # print(pvalue,'--',nvalue)
            while True:
                if nvalue != pvalue :
                    # print("-->",nvalue)
                    break
                else:
                    time.sleep(1)
                    print(".",end="")
                    target = driver.find_element_by_xpath("//label[text()='下一页']")
                    nvalue = target.get_attribute("value")
                    if(target.get_attribute("class")=="end"):
                        break
        except:
            pass
    driver.quit()        

def main():
    url = 'http://fund.eastmoney.com/data/fundranking.html#tzs;c0;r;szzf;pn50;ddesc;qsd20181219;qed20191219;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb'
    url = 'http://fund.eastmoney.com/data/fundranking.html#tall;c0;r;szzf;pn50;ddesc;qsd20181219;qed20191219;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb'

    #股票型基金排行
    gpxurl = "http://fund.eastmoney.com/data/fundranking.html#tgp;c0;r;szzf;pn50;ddesc;qsd20181220;qed20191220;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb"

    #混合型基金排行
    hhurl = "http://fund.eastmoney.com/data/fundranking.html#thh;c0;r;szzf;pn50;ddesc;qsd20181220;qed20191220;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb"

    #指数型基金排行
    zsurl = "http://fund.eastmoney.com/data/fundranking.html#tzs;c0;r;szzf;pn50;ddesc;qsd20181220;qed20191220;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb"
    
    # lof 基金排名
    lofurl = "http://fund.eastmoney.com/data/fundranking.html#tlof;c0;r;szzf;pn50;ddesc;qsd20181220;qed20191220;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb"
    # url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=zs&rs=&gs=0&sc=zzf&st=desc&sd=2018-12-19&ed=2019-12-19&qdii=|&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.3295666930060992'

    # url = 'http://data.eastmoney.com/report/#dHA9MCZjZz0wJmR0PTImcGFnZT00'
    #driver = webdriver.__file__
    getjj(lofurl,"lof.csv")

if __name__ == "__main__":
    main()