# coding:utf-8
import numpy as np
##import pylab as pl
from matplotlib import pyplot as pl
import random as rd
import imageio
import pandas as pd
from pandas.core.frame import DataFrame
from  pandas.testing import assert_frame_equal

'''
标准化数据
'''
def fit_transform(df):
    df = pd.read_csv('./case1.csv',header=0,index_col=0,sep=',')
    df=df.astype(float)#转化数据类型
    df = df.dropna() #删除缺失数据的字段
    df = df.T
    df =df[8:139] #选取每日数据
    std = df.std() #计算标准差, 返回列的标准差
    mean = df.mean()#计算平均值, 返回每列的平均数
    df = (df-mean)/std#标准化数据
    df = df.T
    return df
'''
根据特征值计算“距离”
'''
def distance(a, b):#a,b是Series类型
    #raise Exception
    dis = 0
    for i in range(a.shape[0]):
        dis += (a[i]-b[i])**2
    #print(dis)
    #raise Exception
    return dis

'''
K均值算法
k_point存储每个中心点
'''
def k_means(df, k_count):
    count = df.shape[0]      #行数
    #随机选择K个点
    k = rd.sample(range(count), k_count)
    k_point = DataFrame([df.iloc[i,] for i in k])   #保证有序, 第一组中心点选取从0开始
    #k_point.sort() #以x递增排序
    while True:
        km = [[] for i in range(k_count)]      #存储不同类别
        #遍历所有点
        for i in range(count):
            cp = df.iloc[i,] #当前行
            #计算cp点到所有质心的距离
            _sse = [distance(k_point.iloc[j,], cp) for j in range(k_count)]
            #保存距cp电最近的质心
            min_index = _sse.index(min(_sse))   
            #跟新cp点当前距离最短质心
            km[min_index].append(i)

        #一轮跟新结束, 更换质心
        k_new = []
        #for i in range(k_count):
        #    #_x = sum([x[j] for j in km[i]]) / len(km[i])
        #    #_y = sum([y[j] for j in km[i]]) / len(km[i])
        #    for j in range(pd.shape(1)):
        #print(pd.iloc[0,])
        #raise Exception
        for i in range(k_count):#按列计算平均值
            k_new.append(df.iloc[km[i],].mean())
        #k_new.sort()        #排序

        #print(list(k_new.index))
        #print("---")
        #print(list(k_point.index))
        k_new=DataFrame(k_new)
        #input()
        try:
            #if (k_new != k_point):#一直循环直到聚类中心没有变化
            #    k_point = k_new
            #else:
            #    return km
            assert_frame_equal(k_point,k_new)#相等时退出
            return km
        except Exception :
            k_point = k_new
 
df = pd.read_csv('./case1.csv', header=0, index_col=0,sep=',')
df = fit_transform(df)
k_count = 4
km = k_means(df,k_count)
for i in range(len(km)):
    print('第{0}类:'.format(i+1),df.iloc[km[i],].index.values.tolist())
