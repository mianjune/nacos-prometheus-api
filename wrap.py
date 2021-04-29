# -*- coding: utf-8 -*-

def wrap_services(data: dict):
    if data:
        doms = data.get('doms')
        if doms: return {i: i.split('-') for i in doms}
    return {}


def wrap_service(data: dict):
    """
    https://www.consul.io/api-docs/catalog
    """
    result = []
    if not data: return result
    hosts = data.get('hosts')
    if not hosts: return result

    for h in hosts:
        i = {
            "Address": h['ip'],
            "ServiceAddress": h['ip'],
            "ServiceName": h['serviceName'],
            "ServicePort": h['port'],
            "ServiceID": '{}:{}'.format(h['ip'], h['port']),
            "Meta": {},
        }

        result.append(i)

    return result


def wrap_health_service(data: dict):
    """
    https://www.consul.io/api-docs/health
    """
    result = []
    if not data: return result
    hosts = data.get('hosts')
    if not hosts: return result

    for h in hosts:
        i = {
            "Node": {
                "Address": h['ip'],
            },
            "Service": {
                "Address": h['ip'],
                "Service": h['serviceName'],
                "ID": '{}:{}'.format(h['ip'], h['port']),
                "Port": h['port'],
                "Meta": {},
            }
        }

        result.append(i)

    return result
