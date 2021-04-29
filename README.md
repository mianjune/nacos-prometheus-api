# Nacos Prometheus API

A Nacos open API wraper for [Prometheus](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#consul_sd_config) [Consul API](https://www.consul.io/api-docs/health) Discovery


## Get Start
1. Build Docker image
    - update Nacos host on [nacos_api.py](nacos_api.py), default: [nacos-headless.default:8848](nacos-headless.default:8848)
```console
_image_name='repository-host/nacos-prometheus-api:latest'
docker build -t ${_image_name} .
```

2. Apply Kubernetes component
    - example config file in [k8s/](k8s/)
```console
kubectl apply -f k8s/*.yml
```

