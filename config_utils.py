import os
import configparser


def load_config():
    config_file = r'data_location.config'
    config = configparser.ConfigParser()
    config.read_file(open(config_file))
    return config
