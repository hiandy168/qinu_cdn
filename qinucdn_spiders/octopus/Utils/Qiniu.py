# _*_ coding: utf8 _*_
import urlparse

from octopus.Models.QiniuData import QiniuApkData


def get_apk_size(url=None):
    data = urlparse.urlsplit(url)
    path = data.path
    apk_info = QiniuApkData.objects(id=path[1:]).first()
    if apk_info:
        return apk_info.file_size
    return None
