# coding:utf-8
# 传入数据库
from audioop import add
import json
import time
import hashlib
import pymysql
import requests
import argparse
# 获取时间戳
def getTime():
    return str(int(time.time()))

def addTimes(username,Times):
    sqlTime="UPDATE orderUserList SET Times = '%s' WHERE username = '%s'; " % (Times, username)
    cursor.execute(sqlTime)
    conn.commit()

def fast_book(username, password, bookstatusid,token,loginid,Times):
    # 预约
    headers = {
        'token': token,
        'loginid': loginid,
        'Content-Type': 'application/json;charset=UTF-8'
    }
    payload = json.dumps({})
    timestamp = getTime()
    bookURL = 'http://ligong.deshineng.com:8082/brmclg/api/bathRoom/bookOrder' + "?time=" + timestamp + "&bookstatusid=" + bookstatusid
    bookURL = requests.request("POST", bookURL, headers=headers, data=payload)
    #print(bookURL.json())
    updateTime=bookURL.json()['data']['bookOrderList'][0]['createTimeStr']
    bathRoomName=bookURL.json()['data']['bookOrderList'][0]['bathRoomName']
    orderTime=bookURL.json()['data']['bookOrderList'][0]['period']
    if((bookURL.json()['data']['succeed']=='N')|(bookURL.json()['data']['succeed']=='Q')):
        status=0
    else:
        status=1
    print(status)
    sql="UPDATE orderUserList SET updateTime = '%s', orderTime= '%s', bathRoomName = '%s' WHERE username = '%s' AND password = '%s'; " % (updateTime, orderTime, bathRoomName, username, password)
    cursor.execute(sql)
    conn.commit()
    tmp=int(Times)
    if status==0:
        return 0
    else:
        addTimes(username,str(tmp+1))
        
# 查询数据库
if __name__ == "__main__":
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='bath', password='bathroom',database='bathroom', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    print(cursor)
    # 定义SQL语句
    sql = "SELECT * FROM orderUserList;"
    # 执行SQL语句
    cursor.execute(sql)
    conn.commit()
    searchList = cursor.fetchall()
    
    # 执行预约操作
    for i in searchList:
        if i['token']=='None':
            continue
        if i['bookstatusid'] == '0':
            print(i['username'] + " No request")
            continue
        fast_book(i['username'],i['password'],i['bookstatusid'],i['token'],i['loginid'],i['Times'])
    # 游标对象关闭
    cursor.close()
    # 关闭连接
    conn.close()