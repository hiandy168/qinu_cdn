#!/usr/bin/env python
# --*-- coding:utf-8 --*--


import urllib
import urllib2
import requests
import json

# import requests
#
# ret = requests.get('https://github.com/timeline.json')
#
# print ret.url
# print ret.text

values = { "msgtype": "text",
            "text": {
                "content": u'最后一炮'
            },

            "at": {
                "atMobiles": [
                    "13986238346",
                    "18627051621"
                ],
            # "isAtAll": false

            }


           }


# values = {
#      "msgtype": "markdown",
#      "markdown": {
#          "title":"武汉天气",
#          "text": "#### 武汉天气\n" +
#                  "> 9度，西北风1级，空气良89，相对温度73%\n\n" +
#                  "> ![screenshot](http://image.jpg)\n"  +
#                  "> ###### 10点20分发布 [天气](http://www.thinkpage.cn/) \n"
#
#
#      }
#  }



url = 'https://oapi.dingtalk.com/robot/send?access_token=6e7583cdcb89f266026a21723e52aedd63dd21e8aa2e2c061b35e734759cf920'
# payload = {'some': 'data'}
headers = {'content-type': 'application/json'}  # 开始报错set item是这里的问题,头部如果headers = {'Content-Type: application/json;charset=utf-8'} 就会报错,头信息后面无需再跟charset=utf-8

ret = requests.post(url, data=json.dumps(values), headers=headers)

print ret.text
print ret.cookies

# values = json.dumps({ "msgtype": "text",
#             "text": {
#                 "content": "this is test."
#             },
#             "at": {
#                 "atMobiles": [
#                     "13986238346",
#                     "18627051621"
#                 ],
#
#             }
#            })
#
# print type(values)
#
#
# # values['username'] = "God"
# # values['password'] = "XXXX"
# # 使用了urllib库中的urlencode方法
# data = urllib.urlencode(values)
# url = "https://oapi.dingtalk.com/robot/send?access_token=6e7583cdcb89f266026a21723e52aedd63dd21e8aa2e2c061b35e734759cf920"
# headers = {'Content-Type: application/json;charset=utf-8'}
# try:
#     request = urllib2.Request(url,data,headers)
#     response = urllib2.urlopen(request)
# except Exception as e:
#     print e
# # ret = requests.post(data=json.dumps(xxx))
# # print repr(ret.text)
# print response.read()



# def post(url, data):
#     req = urllib2.Request(url)
#     data = urllib.urlencode(data)
#     #enable cookie
#     opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
#     response = opener.open(req, data)
#     return response.read()
#
# def main():
#     posturl = "https://oapi.dingtalk.com/robot/send?access_token=6e7583cdcb89f266026a21723e52aedd63dd21e8aa2e2c061b35e734759cf920"
#     # data = {'email':'myemail', 'password':'mypass', 'autologin':'1', 'submit':'登 录', 'type':''}
#     data = json.dumps({
#             "msgtype": "text",
#             "text": {
#                 "content": "我就是我, 是不一样的烟火"
#             },
#             "at": {
#                 "atMobiles": [
#                     "15612338827",
#                     "18912323825"
#                 ],
#                 # "isAtAll": false
#             }
#         })
#
#     print type(data)
#     print post(posturl, data)
#
# if __name__ == '__main__':
#     main()


