"""This module has custom settings for Libtech Django backend"""
from pathlib import Path
import json
HOME_DIR = '/opt/config/sites/covidResponseBackend'
JSON_CONFIG_FILE = f"{HOME_DIR}/emailConfig.json"
with open(JSON_CONFIG_FILE) as config_file:
    EMAIL_CONFIG = json.load(config_file)
BASE_CONFIG_FILE = f"{HOME_DIR}/baseConfig.json"
with open(BASE_CONFIG_FILE) as base_config_file:
    BASE_CONFIG = json.load(base_config_file)
AWS_CONFIG_FILE = f"{HOME_DIR}/aws.json"
with open(AWS_CONFIG_FILE) as aws_config_file:
    AWS_CONFIG = json.load(aws_config_file)
SQL_CONFIG = f"{HOME_DIR}/mysqlConfig.cnf"
