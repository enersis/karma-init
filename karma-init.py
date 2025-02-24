from config import Config
import logging
import yaml
import argparse

from helpers import to_selector
from kubernetes import config, client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler()])

parser = argparse.ArgumentParser(description='Initialize karma')
parser.add_argument('--config', type=str, default="config.yaml", help='Path to config file')
args = parser.parse_args()

with open(args.config, "r") as file:
    app_config = Config(**yaml.safe_load(file))

logging.info(f'Karma init initialised with configuration: {app_config}')

try:
    config.load_incluster_config()
except Exception as e:
    config.load_kube_config()

logging.info(f'Loading base config file from {app_config.baseConfigPath}')

with open(app_config.baseConfigPath, "r") as file:
    base_config = yaml.safe_load(file)


with open(app_config.baseConfigPath, 'r') as baseConfig:
    base_config = yaml.safe_load(baseConfig)

v1 = client.CoreV1Api()
selector = app_config.configMapSelector

try:
    # If running incluster. Set local namespace
    with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as ns_file:
        namespace = ns_file.read().strip()
except IOError:
    namespace = app_config.namespace or 'default'


logging.info(f'Listing ConfigMaps in namespace {namespace} with selector {selector}')
configmaps = v1.list_namespaced_config_map(namespace=namespace, label_selector=to_selector(app_config.configMapSelector))

for configmap in configmaps.items:
    logging.info(f'Found ConfigMap: {configmap.metadata.name}')
    server = yaml.safe_load(configmap.data['server'])
    base_config['alertmanager']['servers'].append(server)

logging.info(f'Writing merged configuration to {app_config.outputConfigPath}')
with open(app_config.outputConfigPath, 'w') as outfile:
    yaml.dump(base_config, outfile, default_flow_style=False)
