# _*_ coding: utf8 _*_
import ConfigParser
import os


def get_config(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/site.conf'
    config.read(path)
    return config.get(section, key)


def get_domain_url_list():
    path = os.path.split(os.path.realpath(__file__))[0] + '/domain_url.conf'
    domain_list = []
    f = open(path, 'r')
    for url in f.readlines():
        url = url.strip()
        domain_list.append("%s" % url)
    return domain_list
