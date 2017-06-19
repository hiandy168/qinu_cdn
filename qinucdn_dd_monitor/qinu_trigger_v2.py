#!/usr/bin/env python
# --*-- coding:utf-8 --*--

import codecs
import os
import json
import pickle
import sys
from pymongo import *
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import requests
import json
from qinu_cdn_api import qinu_api

# mail_host = "smtp.exmail.qq.com"         #定义smtp服务器
# mail_host = "monitor.anfan.com"         #定义smtp服务器
mail_host = "localhost"         #定义smtp服务器
mail_to_mult = "lixiang@anfan.com,dpf@anfan.com,smh@anfan.com,pyd@anfan.com,ryp@anfan.com"  #邮件收件人
mail_from = "cdn@monitor.anfan.com"       #邮件发件人
# mail_pass = "Anfen123redhat"            #邮件发件人邮箱密码
# mail_pass = ""            #邮件发件人邮箱密码

params = {
          'server': '192.168.1.163',
          'port': 80,
          }



while True:

    reload(sys)
    sys.setdefaultencoding('utf8') #gb2312,gbk
    # print sys.getdefaultencoding() # 输出当前编码


    def dd_inform(mess_infom):
        # post的组接口
        # url = 'https://oapi.dingtalk.com/robot/send?access_token=6e7583cdcb89f266026a21723e52aedd63dd21e8aa2e2c061b35e734759cf920'
        url = 'https://oapi.dingtalk.com/robot/send?access_token=466422beff8414177cf8c56f14b19f5ce64eba073f633bc339e4634a617e7b67'
        # payload = {'some': 'data'}
        headers = {'content-type': 'application/json'}

        ret = requests.post(url, data=json.dumps(mess_infom), headers=headers)

        return ret.text
        # print ret.cookies



    def Mail(mass_flow):
        # mass_flow.encode('gbk').decode('gbk').encode('utf-8')
        # print mass_flow
        date = time.strftime('%Y-%m-%d %H:%M:%S')
        msg = MIMEText("<h2>%s</h2><br>\n\n<h3>超过100G流量的包,具体信息如下:</h3>\n  %s" % (date, mass_flow),'html', 'utf-8')
        msg['Subject'] = Header("Qiniu CDN trigger", 'utf-8')     #定义邮件主题
        # msg['From'] = mail_from
        msg['From'] = Header("CDN监控报警",'utf-8')
        # msg['To'] = mail_to
        mail_to_list = mail_to_mult.split(',')
        # print mail_to_list
        for mail_to in mail_to_list:
            msg['To'] = mail_to
            # print mail_to

            try:
                s = smtplib.SMTP()                 #创建一个SMTP()对象
                s.connect(mail_host, "25")             #通过connect方法连接smtp主机，非加密方式
                # s.starttls()                    #启动安全传输模式
                # s.login(mail_from,mail_pass)          #邮箱账户登录认证
                s.sendmail(mail_from, mail_to, msg.as_string())   #邮件发送
                s.quit()       #断开smtp连接
            except Exception, e:
                print str(e)

        #链接MongoDB
    def ConMongo(host,port,cur_db):
        client = MongoClient("host",port)
        db = client.cur_db
        table = db.qiniu_item_data
        return table

    # Conn = ConMongo('192.168.1.246',27017,'anfeng_spider')

    client = MongoClient("10.13.71.227",27017)
    db = client["anfeng_spider"]
    Conn = db.qiniu_item_data
    Conn_total_data = Conn.count()
    # print Conn_total_data

    #连接另一张表qiniu_bandwidth_data
    Cost = db.qiniu_bandwidth_data
    Cost_total_data = Cost.count()


    # 获取前一天的带宽去95平均峰值和预测费用

    # for cost in Cost.find({time.strftime('%Y-%m-%d',time.localtime("scrapy_time")):{"$gte":time.strftime('%Y-%m-%d') }}):
    # round(float(4856425955)/1024/1024/1024,4) 显示小数点的后几位,精度
    # 格式化输出显示浮点数,精度展示,%d无法显示,测试 %s可以显示小数点的精度,目前使用format实现
    # 这里不用total 2次循环,因为每天采集只有一条数据,不会有多条数据,所以无需再次套列表,最后循环大列表获取每条数据,在格式化字符串输出,gt_list_total的逻辑

    for cost in Cost.find({}):
        try:
            cost_message = '%d,%d,%d,%d' % (cost["peak95Avrage"],cost["scrapy_time"],cost["day_time"],cost["cost"])
            cost_list = cost_message.split(',')
            print cost_list
            if time.strftime('%Y-%m-%d',time.localtime(int(cost_list[1]))) == time.strftime('%Y-%m-%d'):
                with open('/tmp/qinu.new', 'ab+') as write_file:
                    value = round(float(cost_list[0])/1024/1024/1024,4)
                    pay = round(float(cost_list[3])/10000,6)
                    write_file.write('<h1 style="color:red;">今日去95平均峰值:{traffic}G,预计本月CDN费用:{money}W</h1>'.format(traffic=value,money=pay))
                with open('/tmp/qinu.dd', 'ab+') as write_file_dd:
                    write_file_dd.write('今日去95平均峰值:{traffic_dd}G,预计本月CDN费用:{money_dd}W\n'.format(traffic_dd=value,money_dd=pay))

            else:
                print "当前时间已经超过采集时间,无需报警."
            cost_list = []
        except Exception as e:
            print e


    # 查询mongo item表中总条目
    total_data = Conn.count()
    # 查询mongo item表中流量大于500G的连接

    # [[],[],[]]
    # gt_list = []
    gt_list_total = []


    # 排除重定向的url，没有包的大小
    for item in Conn.find({"flow_value":{"$gt":136870912000}}):
        try:
            flow_message = '%d,%d,%s,%d,%d,%d,%d' % (item["start_time"],item["scrapy_time"],item["url"],item["flow_value"],item["apk_size"],item["download_count"],item["view_count"])
            gt_list = flow_message.split(',')
            print gt_list
            if time.strftime('%Y-%m-%d',time.localtime(int(gt_list[1]))) == time.strftime('%Y-%m-%d'):
            # gt_list.append(flow_message)
            # print gt_list
                gt_list_total.append(gt_list)
            else:
                print "当前时间已经超过采集时间,无需报警."
            gt_list = []
        except Exception as e:
            print e

    print gt_list_total
    print len(gt_list_total)

    with open('/tmp/qinu.new', 'ab+') as write_file:
        gt_number = len(gt_list_total)
        write_file.write('\n<h4>有问题apk下载总个数: %s个</h4><br><h5>请检查如下投放包是否正常:</h5>\n\n<br><table border="1" cellpadding="10"><tr><th>生成时间</th><th>采集时间</th><th>url</th><th>实际流量</th><th>包大小</th><th>下载次数</th><th>访问次数</th></tr>'  % gt_number)


    if len(gt_list_total) == 0:

        print "有问题的apk下载总个数为%s,钉钉无需报警." % gt_number
    else:
        with open('/tmp/qinu.dd', 'ab+') as write_file_dd:
            write_file_dd.write('一天内下载流量大于100G的apk下载总个数: %s个\n请检查如下投放包是否正常:\n生成时间:%s\n采集时间:%s\n\n            url               实际流量(GB)        包大小(MB)        下载次数        访问次数\n'  % (gt_number,time.strftime('%Y-%m-%d',time.localtime(int(gt_list_total[0][0]))),time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(gt_list_total[0][1])))))



    download_total_time = 0
    visit_total_time = 0
    package_total_size = 0
    actual_total_flow = 0

    for number in gt_list_total:
        # print number
	# print time.strftime('%Y-%m-%d',time.localtime(int(number[1])))
	# if time.strftime('%Y-%m-%d',time.localtime(int(number[1]))) == time.strftime('%Y-%m-%d'):

        actual_total_flow += int(number[3])/1024/1024/1024
        package_total_size += int(number[4])/1024/1024
        download_total_time += int(number[5])
        visit_total_time += int(number[6])

       	with open('/tmp/qinu.new', 'ab+') as write_file:
            try:
                # line = 'time : %s\n url : %s\n traffic : %s\n apk_size : %s\n downloadcount : %s\n view_count : %s\n' % (number[0],number[1],number[2],number[3],number[4],number[5])
                # line = '生成时间 : %s\n 采集时间 : %s\n url : %s\n 实际流量 : %sG\n 包大小 : %sM\n 下载次数 : %s\n 访问次数 : %s\n\n' % (time.strftime('%Y-%m-%d',time.localtime(int(number[0]))),time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(number[1]))),number[2],int(number[3])/1024/1024/1024,int(number[4])/1024/1024,number[5],number[6])
               	line = '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (time.strftime('%Y-%m-%d',time.localtime(int(number[0]))),time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(number[1]))),number[2],int(number[3])/1024/1024/1024,int(number[4])/1024/1024,number[5],number[6])

               	# print line
            except Exception as e:
                print e
            write_file.write(line)

        with open('/tmp/qinu.dd', 'ab+') as write_file_dd:
            try:
                # line_dd = '\n%s    %s    %s    %s    %s    %s    %s\n' % (time.strftime('%Y-%m-%d',time.localtime(int(number[0]))),time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(number[1]))),number[2],int(number[3])/1024/1024/1024,int(number[4])/1024/1024,number[5],number[6])
                line_dd = '\n%s    %s    %s    %s    %s\n' % (number[2],int(number[3])/1024/1024/1024,int(number[4])/1024/1024,number[5],number[6])

            except Exception as e:
                print e

            write_file_dd.write(line_dd)

		

    with open('/tmp/qinu.new', 'ab+') as write_file:
        # ab+ 二进制文件追加模式
        # readlines 读取所有
        write_file.write('</table>')
        write_file.seek(0)
        message = write_file.read()
        message.encode('utf-8')
        # write_file.seek(0)

    with open('/tmp/qinu.dd', 'ab+') as write_file_dd:
        write_file_dd.write('\n下载流量超过100G包的总大小是:%sMB\n总实际流量是:%sGB\n总下载次数:%s次\n总访问次数:%s次\n' % (package_total_size,actual_total_flow,download_total_time,visit_total_time))
        write_file_dd.seek(0)
        message_dd = write_file_dd.read()
        message_dd.encode('utf-8')
	
	# for collect_time in write_file.readlines():
	
	# print write_file.readlines()[4].split(' ')[2]
        # if time.strftime('%Y-%m-%d') == write_file.readlines()[4].split(' ')[2]:
        if gt_number > 0:
              values = { "msgtype": "text","text": {"content": message_dd}, "at": {"atMobiles": ["18607169123","13986238346","18627051621","15601277040","13823131241"], } }
              Mail(message)
              dd_inform(values)

              #print "测试邮件已发"
        else:
              print gt_number

    # 这里报警邮件会打印7次重复内容,需要研究下,在加上接口安全认证,不然谁都可以连接就不安全了,研究得出,不使用socket,使用web框架tornado实现对应的API
    # message_api = qinu_api(params["server"],params["port"],json.dumps(message))
    # message_api.main()

    with open('/tmp/qinu.new', 'w+') as write_file:
        clear_file = ''
        write_file.write(clear_file)

    with open('/tmp/qinu.dd', 'w+') as write_file_dd:
        clear_file_dd = ''
        write_file_dd.write(clear_file_dd)


    print "Sleep 14400s..."
    time.sleep(14400)
