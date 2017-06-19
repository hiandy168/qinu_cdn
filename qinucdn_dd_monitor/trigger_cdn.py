#!/usr/bin/env python
# --*-- coding:utf-8 --*--

import os
import sys
import json
from pymongo import MongoClient
from datetime import datetime, date, time

import time
import pexpect
import smtplib
from email.mime.text import MIMEText

mail_host = "smtp.163.com"         #定义smtp服务器
mail_to = "baojingtongzhi@163.com"  #邮件收件人
mail_from = "monitor@163.com"       #邮件发件人
mail_pass = "123456"            #邮件发件人邮箱密码




while True:
    def Mail(error_ip):
        date = time.strftime('%Y-%m-%d %H:%M:%S')
        msg = MIMEText("%s Ping %s failed from 255.252." % (date, error_ip))
        msg['Subject'] = "Ping %s failed." % error_ip    #定义邮件主题
        msg['From'] = mail_from
        msg['To'] = mail_to
        try:
            s = smtplib.SMTP()                 #创建一个SMTP()对象
            s.connect(mail_host, "25")             #通过connect方法连接smtp主机
            s.starttls()                    #启动安全传输模式
            s.login(mail_from,mail_pass)          #邮箱账户登录认证
            s.sendmail(mail_from, mail_to, msg.as_string())   #邮件发送
            s.quit()       #断开smtp连接
        except Exception, e:
            print str(e)
    ip_list = ['192.168.18.10',
        '192.168.18.11',
        '192.168.18.12']

    for ip in ip_list:
        ping = pexpect.spawn('ping -c 1 %s' % ip)
        check = ping.expect([pexpect.TIMEOUT,"1 packets transmitted, 1 received, 0% packet loss"],2)    #2代表超时时间
        if check == 0:
            Mail(ip)
            print "Ping %s failed,Have email." % ip
        if check == 1:
            print "Ping %s successful." % ip
    print "Sleep 10s..."
    time.sleep(10)


def mongo_to_data:
    pass

# client = MongoClient()
# client = MongoClient("192.168.1.246", 27017)
# db = client.anfeng_spider
# collention = db.qinu_item_data
#
#
# for i in collention.find({"url":"http://apk4.anfan.com/6960_1127.apk"}):
#     print i
#
# print collection.find().count()



入库mongodb的python脚本
#链接MongoDB
def ConMongo(host,port,cur_db,username,password):
    client = MongoClient(host,port)
    db = client[cur_db]
    db.authenticate(username,password)
    table = db.qinu_item_data
    return table

def parseLog(file_log,Connection):
    dic = {}
    dl = []
    with open(file_log) as fd:
        for line in fd:
        try:
            tokens = line.strip().split('\t')
            uid = tokens[0]
            server = tokens[1]
            system = tokens[2]
            level = int(tokens[3])
            vip_level = tokens[4]
            ip = tokens[5]
            time = datetime.strptime(tokens[6], "%Y-%m-%d %H:%M:%S")        #将时间字符串转换成时间格式
            action = tokens[7]
            result = json.loads(tokens[8])                        #特殊字符串转换成json格式
            uuid = tokens[9]
        if uid == 'undefined':
            if result["game_user_id"]:
            uid = result["game_user_id"]
        if len(tokens) == 12:
                channel = tokens[11]
        else:
            channel = ''
            dic = {'uid':uid,'server':server,'system':system,'level':level,'vip_level':vip_level,'ip':ip,'time':time,'action':action,'result':result,'uuid':uuid,'channel':channel}
        dl.append(dic)
        if len(dl) == 20000:
            Connection.insert_many(dl)
            dl = []
        except Exception,e:
        print e, line
    if len(dl) > 0:
        Connection.insert_many(dl)

if __name__ == '__main__':
    Conn = ConMongo('localhost',27017,'talefundb','talefun','123456')
    try:
        parseLog(sys.argv[1],Conn)
    except IndexError,e:
        print './%s path_logfile' % os.path.basename(__file__)

注意事项：
(1)insert_many参数是mongodb 3.0.4中新加的，允许你将一个大列表直接insert到mongodb数据库中
(2)脚本中做了限制，如果字典中有2000个值，就向mongodb插入一次数据，这样在效率上得到了保证
