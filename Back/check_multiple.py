# coding:utf-8
import argparse
import pymysql
import base64
import time
import requests
def getTime():
    return str(int(time.time()))
conn = pymysql.connect(host='127.0.0.1', port=3306, user='bath', password='bathroom',database='bathroom', charset='utf8')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

def getCatch():
    sql="SELECT `key` FROM `Catchphase` WHERE id=1;"
    cursor.execute(sql)
    conn.commit()
    searchList = cursor.fetchall()
    for i in searchList:
        return i['key']

if __name__ == "__main__":
    catch=getCatch()
    # 获取参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--otp', help='otp', required=True)
    args = parser.parse_args()
    otp = args.otp
    if(otp != catch):
        print("otp error")
        exit(1)
    # 登录获取token
    sql= "SELECT realName,username,token,loginid FROM orderUserList;"
    cursor.execute(sql)
    conn.commit()
    searchList = cursor.fetchall()
    for i in searchList:
        if i['token']=='None':
            continue
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
            "loginid": i['loginid']
        }
        url = "http://ligong.deshineng.com:8082/brmclg/api/bathRoom/getBookOrderList?_="+getTime()+"&_+"+getTime()
        r = requests.get(url, headers=headers)
        username=i['username']
        realName=i['realName']
        updateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        if r.json()['data']['bookOrderList']==[]:
            print(username + "无预约")
            sql="UPDATE orderUserList SET updateTime = '%s', orderTime= NULL, bathRoomName = NULL, orderTime = NULL WHERE username = '%s'; " % (updateTime, username)
            cursor.execute(sql)
            conn.commit()
            continue
        period = r.json()['data']['bookOrderList'][0]['period']
        bathRoomName = r.json()['data']['bookOrderList'][0]['bathRoomName']
        studentName = r.json()['data']['bookOrderList'][0]['studentName']
        sql="UPDATE orderUserList SET updateTime = '%s', orderTime= '%s', bathRoomName = '%s' WHERE username = '%s'; " % (updateTime, period, bathRoomName, username)
        cursor.execute(sql)
        conn.commit()
        print(f"{realName}, {username}预约成功，预约时间为{period}，预约地点为{bathRoomName}")