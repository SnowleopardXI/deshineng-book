# coding:utf-8
import pymysql
import hashlib
import time
import requests
import json

# 获取时间戳
def getTime():
    return str(int(time.time()))

# 连接数据库
conn = pymysql.connect(host='127.0.0.1', port=3306, user='bath', password='bathroom',database='bathroom', charset='utf8')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

# import headers
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

#Clear data
def clear():
	sql="UPDATE `orderUserList` SET `bathRoomName`=NULL,`orderTime`=NULL;"
	cursor.execute(sql)
	conn.commit()
# 查询数据库
if __name__ == "__main__":
    clear()
    uniqueUserIndex = 'SELECT username,password,realName FROM orderUserList'
    cursor.execute(uniqueUserIndex)
    conn.commit()
    searchList = cursor.fetchall()
    for i in searchList:
        username = i['username']
        password = i['password']
        name = i['realName']
        # 登录获取token
        body={'password':hashlib.md5(str(password).encode()).hexdigest(),
        'code':username}
        loginURL = 'http://ligong.deshineng.com:8082/brmclg/api/logon/login'
        timestamp = getTime()
        login = requests.post(loginURL + "?time=" + timestamp, json=body, headers=headers)
        temp=(login.json()).get('data')
        token=str(temp.get('token'))#获取token
        loginid=str(temp.get('loginid'))#获取登录id
        updateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        # 更新token loginid password
        update="UPDATE orderUserList SET token = '%s', loginid = '%s', updateTime = '%s' WHERE username = '%s' " % (token,loginid,updateTime,username)
        cursor.execute(update)
        conn.commit()
        print(username + " " + name + " update success")
        
    # 游标对象关闭
    cursor.close()
    # 关闭连接
    conn.close()