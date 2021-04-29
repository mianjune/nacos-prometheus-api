# Nacos Prometheus API

[Prometheus](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#consul_sd_config) 基于 [Nacos开放API](https://nacos.io/en-us/docs/open-api.html) 的服务发现的 [Consul API](https://www.consul.io/api-docs/health) 格式代理[接口](#接口样例) 

[English](README.md)

## 开始

- 更新 [nacos_api.py](nacos_api.py) 服务地址, 或指定启动参数`--nacos-servers`, 默认为 [nacos-headless.default:8848](nacos-headless.default:8848)

```console
# 安装Python依赖
pip install -r requirements.txt

# 启动
./run.py
```

- ### 可选: [Kubernetes](https://kubernetes.io/docs/home/) 部署

1. 构建 [Docker](https://docs.docker.com/engine/reference/commandline/build/) 镜像

```console
#!/bin/sh
_image_name='repository-host/nacos-prometheus-api:latest'
docker build -t ${_image_name} .
# docker push ${_image_name}
```

2. 创建 [Kubernetes](https://kubernetes.io/docs/home/) 组件
    - Kubernetes 组件配置参考 [k8s/](k8s/) ， 按需修改

```console
kubectl apply -f k8s/*.yml
```

3. 添加 [Prometheus](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#consul_sd_config) 服务发现配置
    - 参考

```yaml
- job_name: nacos-test
  scheme: http
  metrics_path: '/actuator/prometheus'
  proxy_url: 'http://host-to-nginx-proxy-service:32088'
  consul_sd_configs:
    - server: 'host-to-api-service:80'
      scheme: http
      # 可选, 指定 Nacos 组
      # datacenter: SOME_NACOS_GROUP

      # 可选, tags 过滤，服务名分词
      # tags:
      # - TAG_NAME
  relabel_configs:
    # 可选, 常用label定义
    - source_labels: [ '__meta_consul_service' ]
      target_label: service
    - source_labels: [ '__meta_consul_dc' ]
      target_label: group
    - replacement: test
      target_label: env
```

### 接口样例

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
