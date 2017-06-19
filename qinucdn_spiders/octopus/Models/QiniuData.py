# _*_ coding: utf-8 _*_
from mongoengine import StringField, DynamicDocument, IntField, LongField


class QiniuOriginData(DynamicDocument):
    meta = {'collection': 'qiniu_origin_data'}
    site = StringField(required=True)
    type = StringField(required=True)
    start_time = IntField(required=True)
    end_time = IntField(required=True)
    scrapy_time = IntField(required=True)


class QiniuBucketsData(DynamicDocument):
    meta = {'collection': 'qiniu_buckets_data'}
    id = StringField(required=True, primary_key=True)
    name = StringField(required=True)
    zone = StringField(required=True)
    private = IntField(required=True)
    protected = IntField(required=True)
    last_operation = StringField(required=True)
    last_operation_extra = StringField(required=True)
    last_operation_at = StringField(required=True)
    scrapy_time = IntField(required=True)


class QiniuApkData(DynamicDocument):
    meta = {'collection': 'qiniu_apk_data'}
    id = StringField(required=True, primary_key=True)
    dl_url = StringField(required=True)
    dl_remove_attname_url = StringField(required=True)
    hash = StringField(required=True)
    file_size = LongField(required=True)
    put_time = StringField(required=True)
    mime_type = StringField(required=True)
    scrapy_time = IntField(required=True)


class QiniuRegionData(DynamicDocument):
    meta = {'collection': 'qiniu_region_data'}
    region = StringField(required=True)
    flow = LongField(required=True)
    scrapy_time = IntField(required=True)


class QiniuIpData(DynamicDocument):
    meta = {'collection': 'qiniu_ip_data'}
    ip = StringField(required=True, primary_key=True)
    flow = LongField()
    count = LongField()
    scrapy_time = IntField(required=True)


class QiniuItemData(DynamicDocument):
    meta = {'collection': 'qiniu_item_data'}
    id = StringField(required=True, primary_key=True)
    site = StringField(required=True)
    url = StringField(required=True)
    flow_value = LongField()
    view_count = LongField()
    start_time = IntField(required=True)
    end_time = IntField(required=True)
    scrapy_time = IntField(required=True)


class QiniuBandWidthData(DynamicDocument):
    meta = {'collection': 'qiniu_bandwidth_data'}
    id = LongField(required=True, primary_key=True)
    peak95Avrage = LongField(required=True)
    peakAvrage = LongField(required=True)
    day_time = LongField(required=True)
    scrapy_time = IntField(required=True)
