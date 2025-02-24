# Karma Init

## Overview

This tool is used to read and build server configurations from ConfigMaps and append them to the Karma configuration. It is designed to run as an initContainer in Kubernetes.

## Usage

1. Deploy the initContainer in your Kubernetes pod specification.
2. Ensure the ConfigMaps containing the server configuration are available in the same namespace.
3. The initContainer will read the configurations from the ConfigMap and append them to the Karma configuration file.

## Example

Initialize the application with configuration in the following format 
```yaml
configMapSelector:
  k8s.enersis.ch/type: karma-config
  k8s.enersis.ch/karma-instance: enersis
baseConfigPath: testdata/base.config.yaml
outputConfigPath: testdata/out.yaml
```
Optional option `namespace`, only used for development. Otherwise namespace from `/var/run/secrets/kubernetes.io/serviceaccount/namespace` is read


Initialize the karma base config. .e.g:

```yaml
alertmanager:
  interval: 1m
  servers: []
history:
  timeout: 1m
  rewrite:
    - source: 'http://(.*)'
      uri: 'https://$1'
```

Example ConfigMap with server configuration:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: alertmanager-server-1
  labels:
    k8s.enersis.ch/type: karma-config
    k8s.enersis.ch/karma-instance: enersis
data:
  server: |
    name: madme-prod
    uri: https://alertmanager-v2.gaia.production.euc1.aws.climateintelligence.local
    proxy: false
    readonly: true
```

## Runtime options
The following arguments can be passed to this application:
* `--config`: Path to configuration file in yaml.


