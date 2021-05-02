# -*- coding: utf-8 -*-
from logging import getLogger
from random import choice

import requests

"""
[Nacos API DOC](https://nacos.io/zh-cn/docs/open-api.html)
"""

# 2021-03-30 18:14:55: without [Query Service] API
# import nacos
# client = nacos.NacosClient('nacos.renren.tagtic.cn', namespace=None)
# client.list_naming_instance()

# Nacos host with port
NACOS_HOSTS = ('nacos-headless.default:8848',)

log = getLogger(__name__)


def get_nacos_node(): return choice(NACOS_HOSTS)


def get_service_list(group=None):
    """
    TODO: page rolling...
    """
    r = requests.get('http://%s/nacos/v1/ns/service/list' % get_nacos_node(),
                     params={'pageNo': 1, 'pageSize': 1000, 'groupName': group})
    log.debug('nacos services: %s %s', group, r.text)
    return r.json()


def get_instance_list(service, group=None):
    r = requests.get('http://%s/nacos/v1/ns/instance/list' % get_nacos_node(),
                     params={'pageNo': 1, 'pageSize': 1000, 'groupName': group, 'serviceName': service, 'healthyOnly': True})
    log.debug('nacos instances: %s %s %s', group, service, r.text)
    return r.json()
