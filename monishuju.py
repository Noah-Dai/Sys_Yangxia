#coding:utf-8
#!/usr/bin/python
import sqlite3
from time import sleep
import operator
from numpy import *
import sys
import time

def GetID():
    conn=sqlite3.connect('YXDate.db') # 连接数据库  
    curs=conn.cursor()   
    curs.execute('SELECT * from catalog order by ID desc') #在执行查询语句后，Python将返回一个循环器，包含有查询获得的多个记录。你循环读取，也可以使用sqlite3提供的fetchone()和fetchall()方法读取记录：
    values = curs.fetchone()# 使用 fetchone() 方法获取一条数据库。
    conn.commit()  #执行数据更新
    conn.close()    #关闭数据库
    if not values:   #判定数据库里的数据是不是空的，如果是空的就从i=1开始记录
        i=0 
        print('从第',i+1,'组数据开始记录')#读取的数据，是元组格式，提取方法和列表一样,三者分别为ID号，温度，湿度
        return i
    else :
        i=values[0] 
        print('从第',i+1,'组数据开始记录')#读取的数据，是元组格式，提取方法和列表一样,三者分别为ID号，温度，湿度
        return i   
def setTem():
    SetData=[]
    SetData.append(random.uniform(25, 29))
    SetData.append(random.uniform(54, 56))
    SetData.append(random.randint(0,1))
    return SetData
    sleep(2)
    
def Input_catalog(temps,humis,lable):
    i=GetID()
    conn=sqlite3.connect('YXDate.db')     #连接数据库
    curs=conn.cursor()    
    curs.execute('INSERT INTO catalog VALUES(?,?,?,?,?)',(i,time.strftime("%c"),temps,humis,lable)) #插入数据
    conn.commit()  #执行数据更新       
    conn.close()    #关闭数据库     
    print('Hey,Man! Good Luck.Input_catalog')
    
def Input_catalog1(temps,humis,lable):
    i=GetID()
    conn=sqlite3.connect('YXDate.db')     #连接数据库
    curs=conn.cursor()    
    curs.execute('INSERT INTO catalog1 VALUES(?,?,?,?,?)',(i,time.strftime("%c"),temps,humis,lable)) #插入数据
    conn.commit()  #执行数据更新       
    conn.close()    #关闭数据库     
    print('Hey,Man! Good Luck..Input_catalog1')
    
    
def main():
    
    for n in range(1,500):
        Data=setTem()
        if n%2==1:
            Input_catalog(Data[0],Data[1],Data[2])
            print(Data[0],Data[1],Data[2])
    
        elif n%2==0:
            Input_catalog1(Data[0],Data[1],Data[2])
            print(Data[0],Data[1],Data[2])
    
if __name__=='__main__':
    main()
