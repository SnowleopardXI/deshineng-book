# deshineng-book

## 适用于Tut的自动浴室预约系统（可修改为Tust）

* 环境：Linux、Apache2或nginx、PHP 、MariaDB、Python3
* Python库: pymysql
* PHP 插件: mysqli
* 数据库名称：bathroom，用户名：bath，密码：bathroom
* 数据库各表定义：

  * bookRooms：浴室信息表
    | 列名称 | 作用              |
    | ------ | ----------------- |
    | gender | 性别              |
    | place  | 地点（南区/北区） |
    | time   | 浴室时间段        |
    | bookId | 浴室码            |
  * Catchphase：catchphase信息表
    | 列名称     | 作用       |
    | ---------- | ---------- |
    | id         | id         |
    | updateTime | 更新时间   |
    | key        | catchphase |
  * orderUserList：预约信息表
    | 列名称       | 作用                   |
    | ------------ | ---------------------- |
    | realName     | 储存真实名称，便于查询 |
    | username     | 登录用户名             |
    | password     | 登录密码               |
    | bookstatusid | 预约浴室码             |
    | updateTime   | 状态更新时间           |
    | bathRoomName | 预约浴室名称           |
    | orderTime    | 浴室时间               |
    | Times        | 预约次数               |
    | token        | 登录token              |
    | loginid      | loginid                |
* 文件及目录结构：

```
└── deshineng-book  
  ├──Back  
    ├── book.py：遍历数据库预约表orderUserList，完成预约并将结果写回预约表  
    ├── catch.py：更新catchphase（可选)  
    ├── check_multiple.py：查询所有预约信息  
    ├── check_single.py：查询指定用户预约信息（用户名密码登录验证)  
    ├── commit.py：更新预约信息  
    └── update.py：更新登录状态（token)  
  ├──Front  
    ├──check.htm：检查单用户预约状态  
    ├──check.php：检查单用户预约状态（与Python连接)  
    ├──index.html：主页  
    ├──multi.htm检查多用户预约状态  
    ├──multi.php检查多用户预约状态（与Python连接)  
    └──ver.php：验证登录信息，写入预约表  
  ├── bathroom.sql：数据库SQL文件  
  ├── LICENSE  
  └── README.md
```

## 原理

### 登录

* 前端检查用户名密码是否正确，正确则将登录信息和预约信息保存到预约表

### 刷新

* 使用crontab定期刷新登录状态（本例每天6:30刷新）

### 预约

* 使用crontab每天7点自动遍历预约表，若浴室码为0则不预约

### 查询

* 从浴室表读取预约信息

## 技术性信息

* User-Agent：Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1
* URL：http://ligong.deshineng.com:8082/brmclg

**GNU Public License**
