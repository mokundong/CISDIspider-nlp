# -*- coding: utf-8 -*-
"""
Created on Wed May 24 18:55:39 2017

@author: ben
"""
"""
地址分级
"""
import jieba,csv,xlrd

def AddreIdentify(addStr,addNameList):#地址分级
#    print([w for w in seg_addStr])
    firstAddId=[]
    for indx in range(0,len(addNameList)):#找到所有一级地名
        if addStr.find(addNameList[indx][0])!=-1:
            firstAddId.append(indx)
#    print(firstAddId)
    addIdentify=[]
    for eachId in firstAddId:#将分词后的词语在一级地名对应的二级地名中查找
#        print('...............开始',eachId)
        flag=0
        seg_addStr=jieba.cut(addStr.encode('utf-8'),cut_all=False)
        for w in seg_addStr:#注意，generator用一次后就到尾巴了
            for eachAdd in addNameList[eachId][1]:
#                print(eachAdd,w)
                if eachAdd.find(w)==0:
                    addIdentify.append([addNameList[eachId][0],eachAdd])
                    flag+=1
#                    print(flag)
        if flag==0:
            addIdentify.append([addNameList[eachId][0],''])#如果要更严谨，还需去重
    return addIdentify

#seg_addStr=jieba.cut(addStr.encode('utf-8'),cut_all=False)
#print([w for w in seg_addStr])
#
excelfile = xlrd.open_workbook('省市级名称表.xlsx')
addName = excelfile.sheet_by_name("Sheet1")
Nrows=35
addNameList=[]
for id in range(1,35):
    temp=addName.row_values(id)[1:]
    addNameList.append([addName.row_values(id)[0],temp])
#    
#addStr='山东省江苏省南京市'
#addIdentify11=AddreIdentify(addStr,addNameList)
csvfile = open('项目拟审核公示表.csv', 'r')
reader = csv.reader(csvfile)

projectAddreList=[]
coun=0
for line in reader:
    coun+=1
    if coun!=1:
        addIdentify=AddreIdentify(line[1],addNameList)
        for n in range(0,len(addIdentify)):     
            projectAddreList.append([line[0],line[4],line[1]]+addIdentify[n])
csvfile.close() 
csvfile = open('项目地点信息表.csv', 'w',newline ='')#在windows下如果不加newline=''，将隔行加入数据
writer = csv.writer(csvfile)
writer.writerow(['项目名称'	,'发布日期','建设地点','一级地区','二级地区'])
writer.writerows(projectAddreList)
csvfile.close()