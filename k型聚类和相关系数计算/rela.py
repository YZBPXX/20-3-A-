import pandas as pd
from pandas.plotting import parallel_coordinates
import matplotlib.pyplot as plt
from geopy.distance import geodesic
data = pd.read_csv('./case1.csv',header=0,index_col=0)
'''
选取某些国家计算斯皮尔曼相关系数
'''
def spearman(li): #li 是有Series元素的列表
    #df = pd.DataFrame(li)
    df = data
    df = df.T
    df = df[li]
    df = df[8:139]
    df = (df-df.mean())/df.std() #标准化
    return df.corr(method='spearman')

'''
按相关系数大小排列,获取前k个国家
'''
def maxGroup(df, country, k):
    df = df[[country]].nlargest(k,country)
    return df.index.values

'''
以千米为单位返回两国家距离
'''
def dis(naCountry1,naCountry2):
    port1 = (data['Lat'][naCountry1],data['Long'][naCountry1])
    port2 = (data['Lat'][naCountry2],data['Long'][naCountry2])
    return geodesic(port1,port2).km

'''
计算流动相关系数
'''
def rel(naCountry1, naCountry2):
    E = data['GDP'][naCountry1]/data['GDP'][naCountry2]
    E = 1/(abs(E-1))
    #if (E<1):
    #    E = 1/E
    re = E/dis(naCountry1,naCountry2)
    return re

'''
计算总体流动相关系数
'''
def allRel():
    index = data.index.values
    li = []
    for i in index:
        subli = []
        for j in index:
            if i==j:
                subli.append(float("inf"))
            else :
                subli.append(rel(i,j))
        li.append(subli)
    return pd.DataFrame(li, index=index, columns=index)

# 以南非, 美国, 中国, 巴西, 西班牙为中心, 计算簇群内斯皮尔曼相关系数
countries = ['South Africa','US','China','Brazil','Spain']
for i in countries:
    names = allRel()[[i]].nlargest(10,i).index #获取前10个国家
    df = spearman(names.tolist())
    #df = abs(df)
    path = './rm.csv'
    df.to_csv(path)
    df = pd.read_csv(path)
    plt.figure()
    color = ['maroon','black','gold','DarkSlateGray','darkgreen',
            'MidnightBlue','deeppink','saddlebrown','olive','purple']
    #绘制平行坐标图
    parallel_coordinates(df,'Country/Region',color=color) 
    plt.savefig('./'+i+'.png')



