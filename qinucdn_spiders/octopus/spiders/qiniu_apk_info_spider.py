# _*_ coding: utf8 _*_
import json
import random

import scrapy
import time
from scrapy import Request

from octopus.Models.QiniuData import QiniuBucketsData, QiniuApkData
from octopus.items import QiniuItem
from octopus.site_conf import SiteConfig


class QiniuApkInfoSpider(scrapy.Spider):
    name = "qiniu_apk_info"
    allowed_domains = ["qiniu.com"]
    start_url = "%s?%s" % (SiteConfig.get_config('qiniu.com', 'user_overview_url'),
                           random.randint(100231, 109999),)
    item = QiniuItem(site='qiniu', type='apk_info')

    def start_requests(self):
        headers = {
            "Host": "portal.qiniu.com",
            "User-Agent": "Mozilla/5.0 (Macintosh;Intel Mac OS X 10.12;rv:51.0) Gecko/20100101 Firefox/51.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://portal.qiniu.com/signin",
            "Connection": "keep-alive"
        }
        return [Request(self.start_url, method='GET', meta={'cookiejar': 1},
                        headers=headers, callback=self.parse_overview_cookie)]

    def parse_overview_cookie(self, response):
        qiniu_login_url = SiteConfig.get_config('qiniu.com', 'user_signin_url')
        username = SiteConfig.get_config('qiniu.com', 'username')
        password = SiteConfig.get_config('qiniu.com', 'password')
        body = {
            "username": username,
            "password": password
        }
        return [Request(qiniu_login_url, method='POST', meta={'cookiejar': 1}, body=json.dumps(body),
                        headers=response.headers, callback=self.parse_user_signin)]

    def parse_user_signin(self, response):
        get_user_buckets_list_url = SiteConfig.get_config('qiniu.com', 'user_buckets_list_url')
        user_buckets_list_request = Request(get_user_buckets_list_url, method='GET', meta={'cookiejar': 1},
                                            headers=response.headers, callback=self.parse_buckets_list_request)
        return [user_buckets_list_request]

    # 解析所有的bucket的信息
    def parse_buckets_list_request(self, response):
        if response.status == 200:
            data = json.loads(response.body)
            buckets_list = data['data']
            for bucket in buckets_list:
                get_user_bucket_info_url = SiteConfig.get_config('qiniu.com', 'user_bucket_info_url')
                qiniu_bucket_data = QiniuBucketsData()
                qiniu_bucket_data.name = bucket['name']
                qiniu_bucket_data.zone = bucket['zone']
                qiniu_bucket_data.id = "%s-%s" % (qiniu_bucket_data.zone, qiniu_bucket_data.name)
                qiniu_bucket_data.private = bucket['private']
                qiniu_bucket_data.protected = bucket['protected']
                qiniu_bucket_data.last_operation = bucket['last_operation']
                qiniu_bucket_data.last_operation_extra = bucket['last_operation_extra']
                qiniu_bucket_data.last_operation_at = bucket['last_operation_at']
                qiniu_bucket_data.scrapy_time = int(time.time())
                qiniu_bucket_data.save()

                get_user_bucket_info_url = "%s%s" % (get_user_bucket_info_url, qiniu_bucket_data.name)
                user_bucket_info_url_request = Request(get_user_bucket_info_url, method='GET',
                                                       meta={'cookiejar': 1},
                                                       headers=response.headers,
                                                       callback=self.parse_bucket_info_list_request)
                yield user_bucket_info_url_request

    # 获取各bucket下的文件信息
    def parse_bucket_info_list_request(self, response):
        if response.status == 200:
            data = json.loads(response.body)
            get_user_bucket_content_list_url = SiteConfig.get_config('qiniu.com', 'user_bucket_content_list_url')
            id = "%s-%s" % (data['data']['zone'], data['data']['name'])
            QiniuBucketsData.objects(id=id).update(files=data['data']['files'], storage=data['data']['storage'])
            get_user_bucket_content_list_url = "%s&bucket=%s&limit=1000&marker=" % \
                                               (get_user_bucket_content_list_url, data['data']['name'],)
            user_bucket_content_list_request = Request(get_user_bucket_content_list_url, method='GET',
                                                       meta={'cookiejar': 1, 'bucket_name': data['data']['name']},
                                                       headers=response.headers,
                                                       callback=self.parse_bucket_content_list_request)
            yield user_bucket_content_list_request

    # 解析bucket下的文件列表
    def parse_bucket_content_list_request(self, response):
        if response.status == 200:
            data = json.loads(response.body)
            apks_list = data['data']['entries']
            if apks_list is not None:
                for apk in apks_list:
                    qiniu_apk_data = QiniuApkData()
                    qiniu_apk_data.id = apk['key']
                    qiniu_apk_data.dl_url = apk['dl_url']
                    qiniu_apk_data.dl_remove_attname_url = apk['dl_remove_attname_url']
                    qiniu_apk_data.hash = apk['hash']
                    qiniu_apk_data.file_size = apk['file_size']
                    qiniu_apk_data.put_time = apk['put_time']
                    qiniu_apk_data.mime_type = apk['mime_type']
                    qiniu_apk_data.scrapy_time = int(time.time())
                    qiniu_apk_data.save()

            if data['data']['marker']:
                get_user_bucket_content_list_url = SiteConfig.get_config('qiniu.com', 'user_bucket_content_list_url')
                get_user_bucket_content_list_url = "%s&bucket=%s&limit=50&marker=%s" % \
                                                   (get_user_bucket_content_list_url,
                                                    response.meta['bucket_name'], data['data']['marker'])
                user_bucket_content_list_request = Request(get_user_bucket_content_list_url, method='GET',
                                                           meta={'cookiejar': 1, 'bucket_name': response.meta['bucket_name']},
                                                           headers=response.headers,
                                                           callback=self.parse_bucket_content_list_request)
                yield user_bucket_content_list_request
