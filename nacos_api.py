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

DEFAULT_NAMESPACE = 'public'
DEFAULT_GROUP = 'DEFAULT_GROUP'

# Nacos host with port
NACOS_HOSTS = ('nacos-headless.default:8848',)

log = getLogger(__name__)


def get_nacos_node(): return choice(NACOS_HOSTS)


def get_namespaces():
    r = requests.get('http://%s/nacos/v1/console/namespaces' % get_nacos_node())
    log.debug('nacos namespaces: %s', r.text)
    return r.json()

def get_service_list(namespace=None, group=None):
    """
    TODO: page rolling...
    """
    r = requests.get('http://%s/nacos/v1/ns/service/list' % get_nacos_node(),
                     params={'pageNo': 1, 'pageSize': 1000, 'namespaceId': namespace, 'groupName': group})
    log.debug('nacos [%s.%s] services: %s', namespace or DEFAULT_NAMESPACE, group or DEFAULT_GROUP, r.text)
    return r.json()

def get_all_service_list(namespace=None):
    """
    TODO: page rolling...
    """
    r = requests.get('http://%s/nacos/v1/ns/catalog/services' % get_nacos_node(),
                     params={'pageNo': 1, 'pageSize': 1000, 'namespaceId': namespace})
    log.debug('nacos [%s] services: %s', namespace or DEFAULT_NAMESPACE, r.text)
    return r.json()


def get_instance_list(service, namespace=None, group=None, health_only=False):
    r = requests.get('http://%s/nacos/v1/ns/instance/list' % get_nacos_node(),
            params={'pageNo': 1, 'pageSize': 1000, 'groupName': group, 'namespaceId': namespace, 'serviceName': service, 'healthyOnly': health_only})
    log.debug('nacos [%s.%s.%s] instances: %s', namespace or DEFAULT_NAMESPACE, group or DEFAULT_GROUP, service, r.text)
    return r.json()
