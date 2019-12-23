## 东财基金公司的网站分析  

# 获取所有基金公司的业绩数据放入 all.csv中，[网址](http://fund.eastmoney.com/data/fundranking.html)  
# 然后分析所有基金的业绩排名及公司的业绩排名 

import pandas as pd
import re
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

# 下面分别为股票型，指数型和混合型基金的存档文件
dfgpx = pd.read_csv("gpx.csv",header=None)  
# print(len(dfgpx))
dfzs = pd.read_csv("zs.csv",header=None)  
# print(len(dfzs))
dfhh = pd.read_csv("hh.csv",header=None)  
# print(len(dfhh))
df = dfgpx.append(dfzs,ignore_index=False)
df = df.append(dfhh,ignore_index=False)
# print(len(df))

# 先获取所有的基金业绩信息，然后补全基金代码，填补基金公司
df.columns=["u1","u2","序号","基金代码","基金简称","日期","单位净值","累计净值","日增长率","近1周",
            "近1月","近3月","近6月","近1年","近2年","近3年","今年来","成立来","自定义",
            "手续费","u3"]
df.drop(["u1","u2","u3"],axis=1,inplace=True)
df['基金代码'] = df['基金代码'].map(lambda x : ("000000"+str(x))[-6:])
df.drop_duplicates(["基金代码"],inplace=True)
df.loc[:,"基金公司"]=df["基金简称"].copy().apply(lambda x: x[0:2])
df = df[df['近1年'].str.contains("%")]  #删除近一年没业绩的基金
df = df[df['近1周'].str.contains("%")]  #删除近一年没业绩的基金

df.to_csv("temp.csv")
for i in ["近1周","近1月","近3月","近6月","近1年"]:  #将原表中的字符串改为float以便比较
    df.loc[:,i] = df[i].copy().str.strip("%").astype(float)/100

df1top = df.sort_values(by=["近1年"],ascending=False).head(500) # 选择业绩排名前500的基金
dftemp1 = df1top["基金公司"].value_counts()
dftemp1.name = "top500"
dftemp2 = df["基金公司"].value_counts()
dftemp2.name = "all"
dftemp3 = pd.concat([dftemp1,dftemp2],axis=1,sort=True)  # sort对结果的影响仅在于结果是按哪一列来排序，默认是true
dftemp3.loc[:,"ratio"]=dftemp3["top500"]/dftemp3["all"]
# 取管理基金超过10家的公司，按比例排名，选择前20位
dftemp3 = dftemp3[dftemp3["all"]>10].sort_values(by=["ratio"],ascending=False).head(20)
# print(dftemp3)
companylist = dftemp3.index.tolist()   
print("业绩最好的20家基金公司为：",end="")
print(companylist)

#接下来获取3年内平均业绩最好的20家基金
df3year = df[df['近3年'].str.contains("%")].copy()  #删除近三年没业绩的基金
for i in ["近2年","近3年"]:  #将原表中的字符串改为float以便比较
    df3year.loc[:,i] = df3year.loc[:,i].copy().str.strip("%").astype(float)/100
# df3year.loc[:,'三年业绩汇总']=df3year["近1周"]+df3year["近1月"]+df3year["近3月"]+df3year["近6月"]+df3year["近1年"]+df3year["近2年"]+df3year["近3年"]
df3year.loc[:,'三年业绩汇总']=-df3year["近3月"]+df3year["近6月"]+df3year["近1年"]+df3year["近2年"]+df3year["近3年"]
dfbest = df3year.sort_values(by=["三年业绩汇总"],ascending=False).head(20)

dfbest = dfbest[dfbest["基金公司"].isin(companylist)]
print(dfbest["基金代码"].tolist())

