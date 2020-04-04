import os
import configparser


def load_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_dir, _ = os.path.split(dir_path)
    config_file = r'data_location.config'
    config_path = os.path.join(config_dir, config_file)
    config = configparser.ConfigParser()
    config.read_file(open(config_path))
    return config
