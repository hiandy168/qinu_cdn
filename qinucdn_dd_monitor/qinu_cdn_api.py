#!/usr/bin/env python
# --*-- coding:utf-8 --*--

import socket
import urllib2,urllib
import json
import time,sys
import requests

params = {
          'server': '192.168.1.163',
          'port': 80,
          'data':'api data',
          }

class qinu_api(object):

    def __init__(self,host,port,data):
        self.Host = host
        self.Port = port
        self.data = data

    def handle_request(self,client):
        try:
            buf = client.recv(1024)
            client.send("HTTP/1.1 200 ok\r\n")
            client.send("Content-Type:text/html\r\n\r\n")
            client.send("hello test\r\n")
            #client.send(json.dumps(params))
            client.send(json.dumps(self.data))
        except Exception as e:
            print e

    def main(self):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind((self.Host,self.Port))
        sock.listen(5)

        while True:
            connection,address = sock.accept()
            self.handle_request(connection)
            connection.close()


if __name__ == '__main__':
    qinu = qinu_api(params["server"],params["port"],params['data'])
    qinu.main()
    # main()






