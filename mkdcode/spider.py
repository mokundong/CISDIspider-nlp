# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 09:32:06 2017

@author: mkd
"""

"""
从环评网抓取拟审核项目
"""
import urllib, re, csv
from pyquery import PyQuery as pq
import socket  
import time
  
#获取需要爬取网页的URL地址（所有）         
def GetProjectList(url_cata):
    request = urllib.request.urlopen(url_cata)
    web_text = request.read().decode('utf-8')
    request.close()
    time.sleep(sleepTime)
    reExp = '<li style=\'font-size:14px;\'><span>(.*?)</span><a target="_blank" href="(.*?)"  title="'
    projectTimeandUrlTuple = re.compile(reExp).findall(web_text)
    projectTimeandUrl = []
    for tup in projectTimeandUrlTuple:
        projectTimeandUrl.append(list(tup))
    return projectTimeandUrl
#获取指定时间段内的项目的URL链接列表    
def GetInTimeProject(projectList,beginTime,endTime):
    flag1 = 0
    flag2 = len(projectList)-1
    try:
        while projectList[flag1][0] > endTime:
            flag1 = flag1 + 1
        while projectList[flag2][0] < beginTime:
            flag2 = flag2 - 1
    except Exception as e:
        print('wrong time')
    return projectList[flag1:flag2 + 1]
#表格的爬取需要注意很多细节，表格大小可能会变化。正则表达式可能不能完全抓取所有数据
def getData(projectListInTime,sleepTime):
    projectData=[]
    for url in projectListInTime:
        try:
            request=urllib.request.urlopen(url[1])
            web_text=request.read().decode('utf-8')
        except Exception as e:#出现异常后，重新尝试访问请求
            print(e)
            print('re connecting')
            request.close()
            request=urllib.request.urlopen(url[1])
            web_text=request.read().decode('utf-8')
        request.close()#记得要关闭请求
        time.sleep(sleepTime)#限制访问请求时间间隔
        doc=pq(web_text)
        textTemp=doc('.MsoNormalTable')#这儿又是一个坑！表格的标签不一定一样'tbody'不好用,貌似表的类名一样
        textTemp=textTemp('tr')
        for proNum in range(1,len(textTemp)):
            proData=textTemp.eq(proNum)
            proDataTd=proData('td')
            if proDataTd.eq(1).text() !='':
                projectDataTemp=[proDataTd.eq(1).text(),proDataTd.eq(2).text(),proDataTd.eq(3).text(),proDataTd.eq(5).text(),url[0]]
                projectData.append(projectDataTemp)
        print('已完成',url[0],'日所发布拟审查项目信息的抓取')
    print('finsh')
    return projectData

def saveAsCsv(projectData):
    csvfile = open('项目拟审核公示表.csv', 'w',newline ='')#在windows下如果不加newline=''，将隔行加入数据
    writer = csv.writer(csvfile)
    writer.writerow(['项目名称','建设地点','建设单位','项目概况','发布日期'])
    writer.writerows(projectData)
    csvfile.close()
    
if __name__ == "__main__":   
    timeout = 200  
    sleepTime = 1.5
    beginTime = '2016-01-01'
    endTime='2017-04-05'
    socket.setdefaulttimeout(timeout)#这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置  
    url_cata = 'http://www.zhb.gov.cn/home/rdq/hjyxpj/jsxmhjyxpj/nscxmgs'
    postStr = '/index.shtml'#_1,_2,
    projectList = []
    projectList = GetProjectList(url_cata+postStr)
    for indx in ['/index_1.shtml','/index_2.shtml']:#获取多个页面的项目链接
        projectList += GetProjectList(url_cata+indx)
    for u in range(len(projectList)):#补全链接，因为抓取的每个链接并不是格式相同的，有一些会有缺省
        if projectList[u][1][0] =='.':
            projectList[u][1] = url_cata+projectList[u][1][1:]
    projectListInTime = GetInTimeProject(projectList,beginTime,endTime)  
    projectData = getData(projectListInTime,sleepTime)
    saveAsCsv(projectData)
