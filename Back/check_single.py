# coding:utf-8
import argparse
import pymysql
import hashlib
import time
import requests
def getTime():
    return str(int(time.time()))
conn = pymysql.connect(host='127.0.0.1', port=3306, user='bath', password='bathroom',database='bathroom', charset='utf8')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
def check(username):
    uniqueUserIndex = 'SELECT username FROM orderUserList;'
    cursor.execute(uniqueUserIndex)
    conn.commit()
    searchList = cursor.fetchall()
    for i in searchList:
        if i['username'] == username:
            return 0
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='username', required=True)
    parser.add_argument('-p', '--password', help='password', required=True)
    args = parser.parse_args()
    username = args.username
    password = args.password
    if(check(username)==1):
        print("username error")
        exit(2)
    sql= "SELECT realName,username,token,loginid FROM orderUserList WHERE username = '%s' and password = '%s';" % (username,password)
    cursor.execute(sql)
    conn.commit()
    searchList = cursor.fetchall()
    if len(searchList) == 0:
        print("username or password error")
        exit(2)
    for i in searchList:
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "65",
            "Content-Type": "application/json",
            "Host": "ligong.deshineng.com:8082",
            "Origin": "http://ligong.deshineng.com:8082",
            "Referer": "http://ligong.deshineng.com:8082/brmclg/login.html?v=12&func=null&sn=null",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
            "X-Requested-With": "XMLHttpRequest",
            "token": i['token'],
            "loginid": i['loginid'],
            "username": username,
            "password": password
        }
        realName=i['realName']
        url = "http://ligong.deshineng.com:8082/brmclg/api/bathRoom/getBookOrderList?_="+getTime()+"&_+"+getTime()
        r = requests.get(url, headers=headers)
        updateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        if r.json()['data']['bookOrderList']==[]:
            print(username + "无预约")
            sql="UPDATE orderUserList SET updateTime = '%s', orderTime= NULL, bathRoomName = NULL, orderTime = NULL WHERE username = '%s' AND password = '%s'; " % (updateTime, username, password)
            cursor.execute(sql)
            conn.commit()
            continue
        period = r.json()['data']['bookOrderList'][0]['period']
        bathRoomName = r.json()['data']['bookOrderList'][0]['bathRoomName']
        studentName = r.json()['data']['bookOrderList'][0]['studentName']
        sql="UPDATE orderUserList SET updateTime = '%s', orderTime= '%s', bathRoomName = '%s' WHERE username = '%s' AND password = '%s'; " % (updateTime, period, bathRoomName, username, password)
        cursor.execute(sql)
        conn.commit()
        print(f"{realName}, {username}预约成功，预约时间为{period}，预约地点为{bathRoomName}")
        exit(0)
    # 游标对象关闭
    cursor.close()
    # 关闭连接
    conn.close()