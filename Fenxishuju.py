#coding:utf-8
#!/usr/bin/python
'''
Created on 2017.04.20
@author: Noah
'''
import sqlite3
import time
from numpy import *
import sys

#import matplotlib.pyplot as plt

def GetID():
    conn=sqlite3.connect('YXDate.db') # 连接数据库  
    curs=conn.cursor()   
    curs.execute('SELECT * from catalog order by ID desc') #在执行查询语句后，Python将返回一个循环器，包含有查询获得的多个记录。你循环读取，也可以使用sqlite3提供的fetchone()和fetchall()方法读取记录：
    values = curs.fetchone()# 使用 fetchone() 方法获取一条数据。
    conn.commit()  #执行数据更新
    conn.close()    #关闭数据库
    if not values:   #判定数据库里的数据是不是空的，如果是空的就从i=1开始记录
        i=0 
        #print('从第',i+1,'组数据开始记录')#读取的数据，是元组格式，提取方法和列表一样,三者分别为ID号，温度，湿度
        return i
    else :
        i=values[0] 
        #print('从第',i+1,'组数据开始记录')#读取的数据，是元组格式，提取方法和列表一样,三者分别为ID号，温度，湿度
        return i
#def GetData(): 
       
def loadDataSet():
    dataMat = []; labelMat = []
    i=GetID()
    for n in range(1,i):
        conn=sqlite3.connect('YXDate.db')
        curs=conn.cursor()
        curs.execute('SELECT temp,humi from catalog WHERE ID = ?',(n,))
        values = curs.fetchone()
        conn.commit()
        curs.close()
        conn.close()
        if not values[1]:
            n=n+1
        else:
            dataMat.append([1.0, float(values[0]), float(values[1])])
        #print(n,values[0],values[1])
            labelMat.append(i)
    return dataMat,labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

    
def gradAscent(dataMatIn, classLabels):
    dataMatrix = mat(dataMatIn)             #convert to NumPy matrix
    labelMat = mat(classLabels).transpose() #convert to NumPy matrix
    m,n = shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500
    weights = ones((n,1))
    for k in range(maxCycles):              #heavy on matrix operations
        h = sigmoid(dataMatrix*weights)     #matrix mult
        error = (labelMat - h)              #vector subtraction
        weights = weights + alpha * dataMatrix.transpose()* error #matrix mult
    return weights
    
def plotBestFit(weights):
    import matplotlib.pyplot as plt
    dataMat,labelMat=loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0] 
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i])== 1:
            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = (-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x, y)
    plt.xlabel('X1'); plt.ylabel('X2');
    plt.show()
    
def main():
    dataArr,labelMat=loadDataSet()
    print(gradAscent(dataArr,labelMat))
    weights=gradAscent(dataArr,labelMat)
    plotBestFit(weights.getA())
    #time.sleep(3)
if __name__=='__main__':
    main()
