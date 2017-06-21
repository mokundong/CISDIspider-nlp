# -*- coding: utf-8 -*-
"""
Created on Sat May 27 10:18:55 2017

@author: ben
"""
"""
提取投资总额、环保投入、比例信息
"""
import re,csv

def GetInvestDataByRe(str,reExp1,reExp2):
    str=str.replace(' ','')
    invest=re.compile(reExp1,re.S).findall(str)
    #print('invest:',invest)
    prop=re.compile(reExp2,re.S).findall(str)
    #print('prop:',prop)
    """
    猜想抽取结果仅分成几种情况：
    1、抽到总投资、环保投资、比例
    2、抽到总投资、比例
    3、抽到总投资、环保投资
    4、抽到总投资
    5、抽到比例
    6、项目更新了
    7、都没得
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

#str1='项目拟利用当地煤炭资源，采用 碎煤加压气化、 粉煤加压气化、甲烷化等技术，生产 40 亿标准立方米 / 年合成天然气 ，建设内容包括： （ 1 ）主体工程：固定床碎煤加压气化生产线 3 条，主要包括碎煤气化、净化、甲烷化、煤气水分离、酚氨回收等装置；粉煤气化生产线 1 条，主要包括碎煤气化、净化、甲烷化等装置；硫回收、空分、备煤等装置。（ 2 ）公辅工程：主要包括自备热电站（ 8 台 480 吨 / 小时煤粉锅炉等）、储运系统（油品罐区、圆形料场、灰库等）、脱盐水站、循环水场等。（ 3 ）环保工程：污水处理装置、回用水处理装置、蒸发结晶装置、火炬、危废暂存间等。 拟建工程总投资 289.02 亿元，环保投资 47.60 亿元，占总投资的 16.41% 。'
#str2='项目调整后，主要变更如下： （ 1 ）原油加工规模由 1000 万吨 / 年增至 1300 万吨 / 年。（ 2 ）总体加工工艺路线在原“常减压蒸馏—蜡油加氢裂化—渣油加氢脱硫—重油催化裂化”全加氢工艺的基础上增加了延迟焦化。（ 3 ）项目主体工程仍为 15 套装置，其中渣油加氢脱硫和催化裂化 2 套装置规模不变，新增 1 × 120 万吨 / 年延迟焦化装置、取消 1 × 15 万吨 / 年聚丙烯装置（改由云天化建设），其余常减压、航煤加氢、异构化、硫磺回收等 12 套装置规模增加。（ 4 ） 储罐区储罐由 118 座增至 153 座，总罐容由 179.37 万立方米增至 229.96 万立方米。 （ 5 ）平面布置进行了调整，车用油品质量由欧 IV 升至国 V 。 项目调整后，总投资由 265.7 亿元增至 274.6 亿元，环保投资由 14.38 亿元增至 20.18 亿元，占总投资的比例由 5.4% 增至 7.3% 。'
#str3='本工程为扩建厂址，拟建两台AP1000核电机组以及相应的配套设施，总投资为450亿元人民币，其中环保投资约占整个项目的 10% 。'
#str4='工程开发任务以航运为主，兼顾发电、灌溉、旅游等综合利用效益。水库正常蓄水位55.22米，死水位54.72米，总库容4.073亿立方米，正常蓄水位时库容3.502亿立方米，调节库容0.415亿立方米，具有日调节性能。正常蓄水位时库区回水长度52.67公里，航道渠化后由现状Ⅳ级提高到Ⅲ级。工程枢纽建筑物由船闸、泄水闸、电站厂房、过鱼设施、土坝等组成。河床径流式电站总装机容量74.2兆瓦（7×10.6兆瓦），多年平均发电量2.53亿千瓦时，年利用小时数4290小时。 工程总投资32.46亿元，环境保护投资约27301.25万元。'
#str5='机场场址位于广西玉林市福绵区石和镇，北侧距玉林市直线距离 21 公里。工程为新建国内支线机场，飞行区等级 4C ，设计目标年 2025 年旅客吞吐量为 74 万人次，货邮吞吐量 5000 吨，飞机起降 8132 架次。主要建设内容为新建 1 条长 2600 米跑道， 1 条垂直联络道， 1 个停机坪， 8000 平方米航站楼， 7000 平方米停车场， 1200 平方米货运区。新建 2 座 500 立方米的地面立式储油罐， 1 座汽车加油站，配套建设污水处理站和垃圾转运站等。场外供水、供电、通讯等单独立项建设，不纳入本工程。工程总投资为 16 5135 万元，其中环保投资约为 2236.32 万元，占工程总投资 1.35% 。'
#str=str1[-100:]#投资额都在最后的
#investandProp=GetInvestDataByRe(str)

######正则表达式
reExp1='([0-9. ]+[万亿]元)'#抽取项目总投资和环保投资金额
reExp2='([0-9. ]+%)'#抽取占比
######正则表达式

csvfile = open('项目拟审核公示表.csv', 'r')
reader = csv.reader(csvfile)
investandPropList=[]
coun=0
for line in reader:
    coun+=1
    if coun!=1:
        investandProp=GetInvestDataByRe(line[3][-150:])
        investandPropList.append([line[0],line[3]]+investandProp)
csvfile.close()
csvfile = open('项目投资额信息表.csv', 'w',newline ='')#在windows下如果不加newline=''，将隔行加入数据
writer = csv.writer(csvfile)
writer.writerow(['项目名称'	,'项目概况','总投资','环保投资','环保投资占比'])
writer.writerows(investandPropList)
csvfile.close()