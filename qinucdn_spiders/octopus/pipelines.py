# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

from octopus.Models.QiniuData import QiniuOriginData, QiniuItemData, QiniuRegionData, QiniuIpData, QiniuBandWidthData
from octopus.Utils.Qiniu import get_apk_size


class QiniuPipeline(object):

    def process_item(self, item, spider):
        # 数据解析
        if item['service_type'] == 'top':
            # 原始数据存储
            qiniu_origin_data = QiniuOriginData(site='qiniu', type='cdn-top',
                                                start_time=item['start_time'], end_time=item['end_time'],
                                                scrapy_time=int(time.time()), value=item['value']['traffic'])
            qiniu_origin_data.save()
            all_data = item['value']['traffic']
            # top_flow_url_list = all_data['top_flow_url']
            # top_count_url_list = all_data['top_count_url']
            # top_count_ip_list = all_data['top_count_ip']
            # top_flow_ip_list = all_data['top_flow_ip']
            # top_flow_region_list = all_data['top_flow_region']
            top_flow_url_list = all_data

            if top_flow_url_list is not None:
                for top_flow_url in top_flow_url_list:
                    qiniu_item_data = QiniuItemData()
                    if top_flow_url['key'].endswith('-rwu'):
                        top_flow_url['key'] = top_flow_url['key'].replace('-rwu', '.apk')
                    qiniu_item_data.id = "%s-%s" % (top_flow_url['key'], item['start_time'])
                    qiniu_item_data.site = item['site']
                    qiniu_item_data.type = item['type']
                    qiniu_item_data.start_time = item['start_time']
                    qiniu_item_data.end_time = item['end_time']
                    qiniu_item_data.scrapy_time = int(time.time())
                    qiniu_item_data.url = top_flow_url['key']
                    qiniu_item_data.flow_value = top_flow_url['value']
                    qiniu_item_data.apk_size = get_apk_size(top_flow_url['key'])
                    if qiniu_item_data.apk_size:
                        qiniu_item_data.download_count = qiniu_item_data.flow_value / qiniu_item_data.apk_size
                    qiniu_item_data.save()

            # if top_count_url_list is not None:
            #     for top_count_url in top_count_url_list:
            #         qiniu_item_data = QiniuItemData()
            #         if top_count_url['key'].endswith('-rwu'):
            #             top_count_url['key'] = top_count_url['key'].replace('-rwu', '.apk')
            #         qiniu_item_data.id = "%s-%s" % (top_count_url['key'], item['start_time'])
            #         qiniu_item_data.site = item['site']
            #         qiniu_item_data.type = item['type']
            #         qiniu_item_data.start_time = item['start_time']
            #         qiniu_item_data.end_time = item['end_time']
            #         qiniu_item_data.scrapy_time = int(time.time())
            #         qiniu_item_data.url = top_count_url['key']
            #         qiniu_item_data.view_count = top_count_url['value']
            #         qiniu_item_data.apk_size = get_apk_size(top_count_url['key'])
            #         qiniu_item_data.save()
            #
            # if top_count_ip_list is not None:
            #     for top_count_ip in top_count_ip_list:
            #         qiniu_ip_data = QiniuIpData()
            #         qiniu_ip_data.ip = top_count_ip['key']
            #         qiniu_ip_data.count = top_count_ip['value']
            #         qiniu_ip_data.scrapy_time = int(time.time())
            #         qiniu_ip_data.save()

        elif item['service_type'] == 'top_region':
            top_flow_region_list = item['value']['regions']
            for index, flow_region in enumerate(top_flow_region_list):
                qiniu_region_data = QiniuRegionData()
                qiniu_region_data.region = flow_region
                qiniu_region_data.flow = item['value']['top'][index]
                qiniu_region_data.scrapy_time = int(time.time())
                qiniu_region_data.save()
        elif item['service_type'] == 'top_ip':
            top_ip_list = item['value']['traffic']
            for top_count_ip in top_ip_list:
                qiniu_ip_data = QiniuIpData()
                qiniu_ip_data.ip = top_count_ip['key']
                qiniu_ip_data.count = top_count_ip['value']
                qiniu_ip_data.scrapy_time = int(time.time())
                qiniu_ip_data.save()
        elif item['service_type'] == 'url_viewcount':
            all_data = item['value']['reqcount']
            if all_data is not None:
                for url_viewcount in all_data:
                    qiniu_item_data = QiniuItemData()
                    if url_viewcount['key'].endswith('-rwu'):
                        url_viewcount['key'] = url_viewcount['key'].replace('-rwu', '.apk')
                    qiniu_item_data.id = "%s-%s" % (url_viewcount['key'], item['start_time'])
                    qiniu_item_data.site = item['site']
                    qiniu_item_data.type = item['type']
                    qiniu_item_data.start_time = item['start_time']
                    qiniu_item_data.end_time = item['end_time']
                    qiniu_item_data.scrapy_time = int(time.time())
                    qiniu_item_data.url = url_viewcount['key']
                    qiniu_item_data.view_count = url_viewcount['value']
                    qiniu_item_data.save()
        else:
            qiniu_band_width_data = QiniuBandWidthData()
            qiniu_band_width_data.id = long(item['value']['peak']['time'])/1000
            qiniu_band_width_data.peakAvrage = long(item['value']['peak']['value'])
            qiniu_band_width_data.peak95Avrage = long(item['value']['peak95']['value'])
            qiniu_band_width_data.cost = (long(item['value']['peak95']['value'])/1048576) * 28
            qiniu_band_width_data.day_time = long(item['value']['peak']['time'])/1000
            qiniu_band_width_data.scrapy_time = int(time.time())
            qiniu_band_width_data.save()

        return item
