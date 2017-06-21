# -*- coding: utf-8 -*-
"""
Created on Tue May 23 17:10:16 2017

@author: ben
"""

from pyquery import PyQuery as pq
import csv
#doc=pq(filename='test.html')
##print(doc.html())
#td = doc('.MsoNormalTable')
#td=td('tr')
#td=td.eq(3)
#td=td('td')
#texttd = td.eq(5).text()
#print(texttd)

csvfile = open('csv_test.csv', 'w',newline ='')#在windows下如果不加newline=''，将隔行加入数据
writer = csv.writer(csvfile)
writer.writerow(['姓名', '年龄', '电话'])
data = [
        ['小河', '25', '1234567'],
        ['小芳', '18', '789456'],
        ['小河', '25', '1234567'],
        ['小芳', '18', '789456']
        ]
writer.writerows(data)
csvfile.close()
#csvfile = open('csv_test.csv', 'w',newline ='')#在windows下如果不加newline=''，将隔行加入数据
#writer = csv.writer(csvfile)
#writer.writerow(['项目名称','建设地点','建设单位','项目概况','发布日期'])
#writer.writerows(projectData)
#csvfile.close()
