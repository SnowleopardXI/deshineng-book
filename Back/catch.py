#coding=utf-8
import random
import pymysql
import time
list=['Oberon','Memphis','ladder','Arsenal','citrus','native','Adam','Micaiah','Arthor',
'Steve','Eliorah','Tilon','Shibmah','gebim','Jucal','Uthai','Nymphas','nob',
'Nymphas','zilpah','Asyncritus','uel','Mizar','kenaz','olympas','Ariel','Bellow',
'Loup','Hyde','Cozbi','Lawley','Richard','Kirra','Newton','Eliza','Elizabeth',
'Tesla','Gates','Bill','Jobs','Hussein','eren','Barack','native','ladder']
x=random.sample(list,3)
key = ','.join(x)
updateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
conn = pymysql.connect(host='127.0.0.1', port=3306, user='bath', password='bathroom',database='bathroom', charset='utf8')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
sql="UPDATE Catchphase SET `key` = '%s' ,`updateTime` = '%s' WHERE id=1; " % (key, updateTime)
cursor.execute(sql)
conn.commit()
conn.close()
