#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os.path
import sys
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


def _init_logger(level=logging.DEBUG):
    root = logging.getLogger()
    root.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    root.addHandler(handler)

    from logging import handlers
    logs_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    handler = handlers.TimedRotatingFileHandler(os.path.join(logs_dir, 'api.log'), when='h', interval=4, backupCount=128)
    handler.setFormatter(formatter)
    root.addHandler(handler)


if __name__ == '__main__':
    # _init_logger(logging.DEBUG)
    app.run('0.0.0.0', port=8080)
