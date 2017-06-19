#!/usr/bin/env python
# --*-- coding:utf-8 --*--


from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config

#需要填写你的 Access Key 和 Secret Key
access_key = 'VN1T4HyOswCiFxhsg92BrHU9_oCxmVfvz8PWPW8l'
secret_key = 'LUjILsCuVLX99qMgI8fpPFKIGNgceWMioUfS1_nQ'

#构建鉴权对象
q = Auth(access_key, secret_key)


