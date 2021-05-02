# Nacos Prometheus API

A [Nacos Open API](https://nacos.io/en-us/docs/open-api.html) wrapping as [Consul API](https://www.consul.io/api-docs/health) format for [Prometheus](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#consul_sd_config) Discovery

[中文文档](README_zh.md)

## Get Start

- update Nacos host on [nacos_api.py](nacos_api.py), or specify dynamically by `--nacos-servers`, default is [nacos-headless.default:8848](nacos-headless.default:8848)

```shell
# make sure pypi requirements
pip install -r requirements.txt

# execute
./run.py
```

- start arguments

```shell
# ./run.py -h

usage: run.py [-h] [--log-level LOG_LEVEL] [--log-stdout] [--log-file]
              [--nacos-servers NACOS_SERVERS]

Nacos Consul API server

optional arguments:
  -h, --help            show this help message and exit
  --log-level LOG_LEVEL
                        level for log
  --log-stdout          log to console
  --log-file            log to daily files
  --nacos-servers NACOS_SERVERS
                        the Nacos server host:port[,host2:port], default is "nacos-headless.default:8848"
```

- **Optional:** Deploy on [Kubernetes](https://kubernetes.io/docs/home/)

1. Build [Docker](https://docs.docker.com/engine/reference/commandline/build/) image

```shell
#!/bin/sh
_image_name='repository-host/nacos-prometheus-api:latest'
docker build -t ${_image_name} .
# docker push ${_image_name}
```

2. Apply Kubernetes components
    - example configure files in [k8s/](k8s/), custom and apply them

```shell
kubectl apply -f k8s/*.yml
```

3. Add [Prometheus](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#consul_sd_config) Job
    - example

```yaml
- job_name: nacos-test
  scheme: http
  metrics_path: '/actuator/prometheus'
  proxy_url: 'http://host-to-nginx-proxy-service:32088'
  consul_sd_configs:
    - server: 'host-to-api-service:80'
      scheme: http
      # Optional, filter Nacos group
      # datacenter: SOME_NACOS_GROUP

      # Optional, filter tags that splitting service name words
      # tags:
      # - TAG_NAME
  relabel_configs:
    # Optional, basic labels I recommend 
    - source_labels: [ '__meta_consul_service' ]
      target_label: service
    - source_labels: [ '__meta_consul_dc' ]
      target_label: group
    - replacement: test
      target_label: env
```

## API respond Examples

- [/v1/agent/self](/v1/agent/self)

```json
{
  "Config": {
    "Datacenter": "default"
  }
}

```

- [/v1/catalog/services](/v1/catalog/services)

```json
{
  "service-demo": [
    "service",
    "demo"
  ],
  "service-work": [
    "service",
    "work"
  ]
}
```

- [/v1/health/service/service-demo](/v1/catalog/health/service-demo)

```json
[
  {
    "Node": {
      "Address": "10.244.1.1"
    },
    "Service": {
      "Address": "10.244.1.1",
      "ID": "10.244.1.1:8080",
      "Meta": {
      },
      "Port": 8080,
      "Service": "DEFAULT_GROUP@@service-demo"
    }
  }
]
```

- [/v1/catalog/service/service-demo](/v1/catalog/service/service-demo)

```json
[
  {
    "Address": "10.244.1.1",
    "Meta": {},
    "ServiceAddress": "10.244.1.1",
    "ServiceID": "10.244.1.1:8080",
    "ServiceName": "DEFAULT_GROUP@@service-demo",
    "ServicePort": 8080
  }
]
```
