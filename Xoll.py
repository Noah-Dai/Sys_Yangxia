#coding:utf-8
#!/usr/bin/python
'''
Created on 2016.12.20
@author: Noah
'''
import sys
import serial
from time import sleep
import re
import sqlite3
import time

times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())#获取时间函数,改进后，并没用到此函数
def convert(value):
    if value.startswith('[\''):
        return value.strip('[\'')
    if not value:
        return float(value)#此函数最终并未用到
        
ser= serial.Serial("/dev/ttyAMA0",115200)#从ZigBee串口得到数据
def recv(serial):   
    while True:
        data=serial.read(22)#读串口数据的字节数为26
        if not data:
            print("waiting next signal")
            continue
        else:
            break
        sleep(6)
    return data
def convert1(value):#判断筛选有效数据
    if not value:
        print('There is No Data')
    elif value[0]==' ':       
        print('This is Null')
    else:
        return value[0]#被正则提取数字后，自动变成列表格式['']，取出列表中的数据
    
def insert_data(temp,humi):  #此段函数，留作以后使用，是一段插入数据的函数    
    # 插入数据库  
    temp = "%.1f" %(temp)
    humi = "%.1f" %(humi)   
    curs.execute("INSERT INTO catalog(tdatetime,temp,humi) VALUES((?,?,?))", (temp,humi))  
    conn.commit()  
      
    # 关闭数据库  
    conn.close()  
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
    
def main():   
    i=GetID()
    while True:
        data =recv(ser)
        data1 = data.decode(encoding='utf-8', errors='strict')#将字节解码成UTF-8的编码形式的字符串
        temp =re.findall(r'E(.+?)F',data1)
        humi =re.findall(r'G(.+?)H',data1)#13
        temps = convert1(temp)
        humis = convert1(humi)
        temp1 =re.findall(r'A(.+?)B',data1)#12
        humi1 =re.findall(r'C(.+?)D',data1)
        temps1 = convert1(temp1)
        humis1 = convert1(humi1)
        
        i=i+1           #记录ID
        
        #print(times)   #测试用的显示语句
        print(time.strftime("%c"))
        print('ZigBee收集的数据',data1)    #测试用的显示语句
        print('节点1的数据',temps,humis)    #测试用的显示语句
        print('节点2的数据',temp1,humi1)    #测试用的显示语句
        
        
        conn=sqlite3.connect('YXDate.db')     #连接数据库
        #print("Table connect successfully") #测试用的显示语句
        
        curs=conn.cursor()    
        curs.execute('INSERT INTO catalog VALUES(?,?,?,?)',(i,time.strftime("%c"),temps,humis)) #插入数据
        curs.execute('INSERT INTO catalog1 VALUES(?,?,?,?)',(i,time.strftime("%c"),temps1,humis1)) #插入数据

        conn.commit()  #执行数据更新
        #print("Database Record successfully") #测试用的显示语句
          
        conn.close()    #关闭数据库
        #print("Database close successfully") #测试用的显示语句       
        print('Hey,Man! Good Luck')
        sleep(10)
if __name__=='__main__':
    main()
