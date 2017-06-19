# _*_ coding: utf8 _*_
import json
import random

import scrapy
import time
from scrapy import Request

from octopus.items import QiniuItem
from octopus.site_conf import SiteConfig
from octopus.site_conf.SiteConfig import get_domain_url_list


class QiniuSpider(scrapy.Spider):
    name = "qiniu"
    allowed_domains = ["qiniu.com"]
    start_url = "%s?%s" % (SiteConfig.get_config('qiniu.com', 'user_overview_url'),
                           random.randint(100231, 109999),)
    item = QiniuItem(site='qiniu', type='top_list', service_type='top')
    region_item = QiniuItem(site='qiniu', type='top_list', service_type='top_region')
    ip_item = QiniuItem(site='qiniu', type='top_list', service_type='top_ip')
    url_viewcount_item = QiniuItem(site='qiniu', type='top_list', service_type='url_viewcount')
    ip_viewcount_item = QiniuItem(site='qiniu', type='top_list', service_type='ip_viewcount')
    bandwidth_item = QiniuItem(site='qiniu', type='top_list', service_type='bandwidth')

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
        get_user_fushion_report_url = SiteConfig.get_config('qiniu.com', 'user_fushion_report_url')
        user_fushion_report_request = Request(get_user_fushion_report_url, method='GET', meta={'cookiejar': 1},
                                              headers=response.headers, callback=self.parse_fushion_report)
        return [user_fushion_report_request]

    def parse_fushion_report(self, response):
        now = time.time()
        end_time = int(now - (now % 86400) + time.timezone)
        start_time = end_time - 86400
        start_date = time.strftime('%Y-%m-%d-00-00', time.localtime(start_time))
        # end_date = time.strftime('%Y-%m-%d-00-00', time.localtime(end_time))
        end_date = start_date
        domain_url_list = get_domain_url_list()
        body = {
            "domains": domain_url_list,
            "startDate": start_date,
            "endDate": end_date,
            "region": ['global'],
            "type": "traffic"
        }
        get_user_tops_url = SiteConfig.get_config('qiniu.com', 'user_tops_url')
        qiniu_top_request = Request(get_user_tops_url, method='POST', meta={'cookiejar': 1}, body=json.dumps(body),
                                    headers=response.headers, callback=self.parse_qiniu_top_list)
        self.item['start_time'] = start_time
        self.item['end_time'] = end_time

        url_viewcount_body = {
            "domains": domain_url_list,
            "startDate": start_date,
            "endDate": end_date,
            "region": ['global'],
            "type": "reqcount"
        }
        print start_date
        print end_date
        get_url_view_count_tops_url = SiteConfig.get_config('qiniu.com', 'user_tops_url')
        qiniu_url_viewcount_request = Request(get_url_view_count_tops_url, method='POST', meta={'cookiejar': 1},
                                              body=json.dumps(url_viewcount_body),
                                              headers=response.headers, callback=self.parse_qiniu_url_viewcount_list)
        self.url_viewcount_item['start_time'] = start_time
        self.url_viewcount_item['end_time'] = end_time

        # user_top_region_url
        top_region_body = {
            "domains": domain_url_list,
            "startDate": start_date,
            "endDate": end_date,
            "region": ['global']
        }
        get_user_top_region_url = SiteConfig.get_config('qiniu.com', 'user_top_region_url')
        qiniu_top_region_request = Request(get_user_top_region_url, method='POST', meta={'cookiejar': 1},
                                           body=json.dumps(top_region_body), headers=response.headers,
                                           callback=self.parse_qiniu_top_region_list)
        self.region_item['start_time'] = start_time
        self.region_item['end_time'] = end_time

        # user_top_ip_url
        get_user_top_ip_url = SiteConfig.get_config('qiniu.com', 'user_top_ip_url')
        qiniu_top_ip_request = Request(get_user_top_ip_url, method='POST', meta={'cookiejar': 1},
                                       body=json.dumps(body), headers=response.headers,
                                       callback=self.parse_qiniu_top_ip_list)
        self.ip_item['start_time'] = start_time
        self.ip_item['end_time'] = end_time

        # top ip viewcount
        # ip_viewcount_body = {
        #     "domains": domain_url_list,
        #     "startDate": start_date,
        #     "endDate": end_date,
        #     "region": ['global'],
        #     "type": "reqcount"
        # }
        # get_top_ip_viewcount_url = SiteConfig.get_config('qiniu.com', 'user_top_ip_url')
        # qiniu_top_ip_viewcount_request = Request(get_top_ip_viewcount_url, method='POST', meta={'cookiejar': 1},
        #                                          body=json.dumps(ip_viewcount_body), headers=response.headers,
        #                                          callback=self.parse_qiniu_top_ip_viewcount_list)
        # self.ip_item['start_time'] = start_time
        # self.ip_item['end_time'] = end_time

        # 获取前一天的带宽峰值
        time_local = time.localtime(start_time)
        start = time.strftime("%Y%m%d000000", time_local)
        get_peak_bandwidth_url = SiteConfig.get_config('qiniu.com', 'peak_bandwidth_url')
        domain_url_list = get_domain_url_list()
        print domain_url_list
        peak_bandwidth_request_body = {
            "domains": domain_url_list,
            "g": '5min',
            "start": start,
            "end": start
        }
        qiniu_peak_bandwidth_request = Request(get_peak_bandwidth_url, method='POST', meta={'cookiejar': 1},
                                               body=json.dumps(peak_bandwidth_request_body),
                                               headers=response.headers, callback=self.parse_peak_bandwidth)
        return [qiniu_top_request, qiniu_peak_bandwidth_request, qiniu_top_region_request, qiniu_top_ip_request,
                qiniu_url_viewcount_request]

    def parse_qiniu_top_list(self, response):
        response = json.loads(response.body)
        self.item['value'] = response['data']
        yield self.item

    def parse_qiniu_top_region_list(self, response):
        response = json.loads(response.body)
        self.region_item['value'] = response['data']
        yield self.region_item

    def parse_qiniu_top_ip_list(self, response):
        response = json.loads(response.body)
        self.ip_item['value'] = response['data']
        yield self.ip_item

    def parse_qiniu_url_viewcount_list(self, response):
        response = json.loads(response.body)
        self.url_viewcount_item['value'] = response['data']
        yield self.url_viewcount_item

    # def parse_qiniu_top_ip_viewcount_list(self, response):
    #     response = json.loads(response.body)
    #     self.ip_viewcount_item['value'] = response['data']
    #     yield self.ip_viewcount_item

    # def parse_all_domain_url(self, response):
    #     response = json.loads(response.body)
    #     domain_infos = response['domainInfos']
    #     domain_url_list = []
    #     for domain in domain_infos:
    #         domain_url_list.append(domain['name'])

    def parse_peak_bandwidth(self, response):
        response = json.loads(response.body)
        self.bandwidth_item['value'] = response['data']
        yield self.bandwidth_item
