# coding:utf-8
''' code 1 means otp error
    code 2 means username error
    code 3 means password error
'''
import base64
import argparse
import pymysql
import hashlib
import time
import requests
def getTime():
    return str(int(time.time()))

conn = pymysql.connect(host='127.0.0.1', port=3306, user='bath', password='bathroom',database='bathroom', charset='utf8')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
# 查询数据库中是否存在该用户
def check(username):
    uniqueUserIndex = 'SELECT username FROM orderUserList;'
    cursor.execute(uniqueUserIndex)
    conn.commit()
    searchList = cursor.fetchall()
    for i in searchList:
        if i['username'] == username:
            return 1

def checkId(gender,timep,place):
    sql="SELECT * FROM `bookRooms`WHERE `gender`= '%s' AND `place`='%s' AND `time`='%s';"  % (gender, place, timep)
    cursor.execute(sql)
    conn.commit()
    searchList = cursor.fetchall()
    for i in searchList:
        return i['bookId']
def getCatch():
    sql="SELECT `key` FROM `Catchphase` WHERE id=1;"
    cursor.execute(sql)
    conn.commit()
    searchList = cursor.fetchall()
    for i in searchList:
        return i['key']
# 查询数据库
if __name__ == "__main__":
    catch=getCatch()
    # 获取参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='username', required=True)
    parser.add_argument('-p', '--password', help='password', required=True)
    parser.add_argument('-o', '--otp', help='otp', required=True)
    parser.add_argument('-g', '--gender', help='gender', required=True)
    parser.add_argument('-t', '--timep', help='time', required=True)
    parser.add_argument('-r', '--place', help='place', required=True)
    #parser.add_argument('-e', '--dev', help='developer', required=False)
    args = parser.parse_args()
    username = args.username
    password = args.password
    gender= args.gender
    place= args.place
    timep=args.timep
    #bookstatusid = args.bookstatusid
    bookstatusid=checkId(gender,timep,place)
    otp = args.otp
    if(otp != catch):
        print("otp error")
        exit(1)
    # 登录获取token
    body={'password':hashlib.md5(str(password).encode()).hexdigest(),
        'code':username}
    loginURL = 'http://ligong.deshineng.com:8082/brmclg/api/logon/login'

    timestamp = getTime()
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
        }
    login = requests.post(loginURL + "?time=" + timestamp, json=body, headers=headers)
    temp=(login.json()).get('data')
    token=str(temp.get('token'))#获取token
    loginid=str(temp.get('loginid'))#获取登录id
    if len(token) < 100:
        print("username or password error")
        exit(3)
    # 查询数据库中是否存在该用户
    if(check(username) == 1):
        # 更新token loginid password
        update="UPDATE orderUserList SET token = '%s', loginid = '%s', password = '%s', bookstatusid = '%s' WHERE username = '%s' " % (token,loginid,password,bookstatusid,username)
        cursor.execute(update)
        conn.commit()
        print(username + " update success at " + time.strftime("%a %b %d %I:%M:%S %p %Z", time.localtime()))
    else:
        # 插入数据库
        sql = "INSERT INTO orderUserList(username,password,token,bookstatusid,loginid) VALUES ('%s','%s','%s','%s','%s')" % (username,password,token,bookstatusid,loginid)
        cursor.execute(sql)
        print(username + " login success at " + time.strftime("%a %b %d %I:%M:%S %p %Z", time.localtime()))
    
    conn.commit()
    # 游标对象关闭
    cursor.close()
    # 关闭连接
    conn.close()