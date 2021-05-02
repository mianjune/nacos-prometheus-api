#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import logging
import time

from flask import Flask, jsonify, request
from flask.wrappers import Response

from nacos_api import get_service_list, get_instance_list
from wrap import wrap_services, wrap_service, wrap_health_service

app = Flask(__name__)


@app.route('/v1/agent/self')
def api_agent():
    return jsonify({'Config': {"Datacenter": "default"}})


@app.route('/v1/catalog/services')
def api_services():
    group = request.args.get('dc')
    data = get_service_list(group=group)
    logging.debug('get_service_list: %s', data)

    result = wrap_services(data)
    return jsonify(result)


def api_service_handle(dc: str, _wrap):
    """
    wrap Consul `dc` to Nacos `group`
    :param dc: consul datacenter
    :param _wrap: wrap Nacos response to Consul format
    :return:
    """
    group = request.args.get('dc')
    data = get_instance_list(dc, group=group)
    logging.debug('get_instance_list: %s %s', dc, data)

    result = _wrap(data)

    return jsonify(result)


@app.route('/v1/catalog/service/<string:name>')
def api_service(name):
    return api_service_handle(name, wrap_service)


@app.route('/v1/health/service/<string:name>')
def api_health_service(name):
    return api_service_handle(name, wrap_health_service)


@app.after_request
def after(response: Response):
    response.headers['X-Consul-Index'] = int(time.time() * 1000)
    # logging.debug('respond: %s', response.get_data())
    return response


def _init_logger(level=logging.DEBUG, is_stdout=False, is_file=False):
    root = logging.getLogger()
    root.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if is_stdout:
        import sys
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        root.addHandler(handler)

    if is_file:
        from logging import handlers
        import os
        logs_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        handler = handlers.TimedRotatingFileHandler(os.path.join(logs_dir, 'api.log'), when='h', interval=4, backupCount=128)
        handler.setFormatter(formatter)
        root.addHandler(handler)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Nacos Consul API server')
    p.add_argument('--log-level', default='INFO', help='level for log')
    p.add_argument('--log-stdout', default=False, action='store_true', help='log to console')
    p.add_argument('--log-file', default=False, action='store_true', help='log to daily files')
    p.add_argument('--nacos-servers', action='append', help='the Nacos server host:port[,host2:port], default is "nacos-headless.default:8848"')

    args = p.parse_args()

    _init_logger(level=args.log_level, is_stdout=args.log_stdout, is_file=args.log_file)

    if args.nacos_servers:
        hosts = tuple(h for i in args.nacos_servers for h in i.split(',') if h)
        if hosts:
            import nacos_api
            nacos_api.NACOS_HOSTS = hosts

    app.run('0.0.0.0', port=8080)
