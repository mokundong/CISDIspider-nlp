# -*- coding: utf-8 -*-
"""
Created on Mon May 22 15:16:34 2017

@author: ben
"""
"""
从环评网抓取拟审核项目
"""
import os, urllib, re, csv
from pyquery import PyQuery as pq
import socket  
import time  
timeout = 200  
sleepTime=1.5  
socket.setdefaulttimeout(timeout)#这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置  
headers = {
              }
def WriteText(filename,text):
    if os.path.exists(filename):
        os.remove(filename)
    try:
        fp=open(filename,'w')
        fp.write(text)
    except Exception as e:
        print(e)
        fp.close()
    fp.close()
def GetProjectList(url_cata):#项目数据存放在两个服务器上 hps.mep和www.zhb，一个服务器的地址简写了
#    resp=urllib.request.Request(url_cata,headers=headers)
    request=urllib.request.urlopen(url_cata)
    web_text=request.read().decode('utf-8')
    request.close()#记得要关闭请求
    time.sleep(sleepTime)
#    WriteText('test.txt',web_text)
    reExp='<li style=\'font-size:14px;\'><span>(.*?)</span><a target="_blank" href="(.*?)"  title="'
    projectTimeandUrlTuple=re.compile(reExp).findall(web_text)
    projectTimeandUrl=[]
    for tup in projectTimeandUrlTuple:
        projectTimeandUrl.append(list(tup))
    return projectTimeandUrl
def GetInTimeProject(projectList,beginTime,endTime):#筛选时间段内的项目链接
    flag1=0
    flag2=len(projectList)-1
    try:
        while projectList[flag1][0]>endTime:
            flag1=flag1+1
        while projectList[flag2][0]<beginTime:
            flag2=flag2-1
    except Exception as e:
        print('日期不对')
    return projectList[flag1:flag2+1]
    
url_cata='http://www.zhb.gov.cn/home/rdq/hjyxpj/jsxmhjyxpj/nscxmgs'
postStr='/index.shtml'#_1,_2
projectList=[]
projectList=GetProjectList(url_cata+postStr)
for indx in ['/index_1.shtml','/index_2.shtml']:#获取几个页面的项目链接
    projectList+=GetProjectList(url_cata+indx)
for u in range(len(projectList)):#补全链接
    if projectList[u][1][0] =='.':
        projectList[u][1]=url_cata+projectList[u][1][1:]
beginTime='2016-01-01'
endTime='2017-04-05'
projectListInTime=GetInTimeProject(projectList,beginTime,endTime)
#def GetDataFromUrl(projectListInTime):#表格的爬取需要注意很多细节，表格大小可能会变化。正则表达式可能不能完全抓取所有数据
projectData=[]
for url in projectListInTime:
#    resp=urllib.request.Request(url[1],headers=headers)
    try:
        request=urllib.request.urlopen(url[1])
        web_text=request.read().decode('utf-8')
    except Exception as e:#出现异常后，重新尝试访问请求
        print(e)
        print('尝试重新连接')
        request.close()
        request=urllib.request.urlopen(url[1])
        web_text=request.read().decode('utf-8')
    request.close()#记得要关闭请求
    time.sleep(sleepTime)#限制访问请求时间间隔
#    #抽取名称信息，正则不好用
#    reExp1='<tr style.*?width=".*?".*?10.5pt">.*?</span></p>.*?width=".*?".*?10.5pt">(.*?)</span></p>.*?width=".*?".*?10.5pt">(.*?)</span></p>.*?width=".*?".*?10.5pt">(.*?)</span></p>.*?width=".*?".*?10.5pt">(.*?)</sp'
#    projectDataTuple=re.compile(reExp1,re.S).findall(web_text)
#    #抽取项目概况信息，需经过多次抽取
#    #web中表格的格式不一，很难用正则表达式抽取信息。学习PyQuery和BeautifulSoup
#    reExp2='<td width="224".*?10.5pt">(.*?)</span>'
##   projectDetailTuple=re.compile(reExp2,re.S).findall(web_text)
    #利用pyquery抽取信息
    doc=pq(web_text)
    textTemp=doc('.MsoNormalTable')#这儿又是一个坑！表格的标签不一定一样'tbody'不好用,貌似表的类名一样
    textTemp=textTemp('tr')
    for proNum in range(1,len(textTemp)):
        proData=textTemp.eq(proNum)
        proDataTd=proData('td')
        if proDataTd.eq(1).text() !='':
            projectDataTemp=[proDataTd.eq(1).text(),proDataTd.eq(2).text(),proDataTd.eq(3).text(),proDataTd.eq(5).text(),url[0]]
            projectData.append(projectDataTemp)
    print('已完成',url[0],'所发布拟审查项目信息的抓取')
print('抓取任务完成')
csvfile = open('项目拟审核公示表.csv', 'w',newline ='')#在windows下如果不加newline=''，将隔行加入数据
writer = csv.writer(csvfile)
writer.writerow(['项目名称','建设地点','建设单位','项目概况','发布日期'])
writer.writerows(projectData)
csvfile.close()
