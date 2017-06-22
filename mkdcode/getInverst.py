# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 10:29:51 2017

@author: mkd
"""

import re,csv

def GetInvestDataByRe(str,reExp1,reExp2):
    str=str.replace(' ','')
    invest=re.compile(reExp1,re.S).findall(str)
    prop=re.compile(reExp2,re.S).findall(str)
    """
    猜想抽取结果仅分成几种情况：
    1、抽到总投资、环保投资、比例
    2、抽到总投资、比例
    3、抽到总投资、环保投资
    4、抽到总投资
    5、抽到比例
    6、项目更新了
    7、都没有
    """
    M=len(invest)
    N=len(prop)
    investandProp=[]
    if (M==2) & (N==1):#情况1
        investandProp.extend([invest[0].strip(),invest[1].strip(),prop[0].strip()])
    elif (M==1) & (N==1):#情况2
        investandProp.extend([invest[0].strip(),'',prop[0].strip()])
    elif (M==2) & (N==0):#情况3
        investandProp.extend([invest[0].strip(),invest[1].strip(),''])
    elif (M==1) & (N==0):#情况4
        investandProp.extend([invest[0].strip(),'',''])
    elif (M==0) & (N==1):#情况5
        investandProp.extend(['','',prop[0].strip()])
    elif (M==4) & (N==2):#情况6
        investandProp.extend([invest[1].strip(),invest[3].strip(),prop[1].strip()])
    elif (M==0) & (N==0):#情况7
        investandProp.extend(['','',''])
    else:
        investandProp.extend([invest[-2].strip(),invest[-1],prop[-1]])
    return investandProp

def saveAsCsv(investandPropList):
    csvfile = open('项目投资额信息表.csv', 'w',newline ='')#在windows下如果不加newline=''，将隔行加入数据
    writer = csv.writer(csvfile)
    writer.writerow(['项目名称'	,'项目概况','总投资','环保投资','环保投资占比'])
    writer.writerows(investandPropList)
    csvfile.close()

if __name__ == "__main__":
    reExp1='([0-9. ]+[万亿]元)'#抽取项目总投资和环保投资金额
    reExp2='([0-9. ]+%)'#抽取占比
    
    csvfile = open('项目拟审核公示表.csv', 'r')
    reader = csv.reader(csvfile)
    investandPropList=[]
    coun=0
    for line in reader:
        coun+=1
        if coun!=1:
            investandProp=GetInvestDataByRe(line[3][-150:],reExp1,reExp2)
            investandPropList.append([line[0],line[3]]+investandProp)
    csvfile.close()
    
    saveAsCsv(investandPropList)
