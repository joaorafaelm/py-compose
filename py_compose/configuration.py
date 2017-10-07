from os.path import isfile
import yaml

CONFIG_FILE = 'py-compose.yaml'


class Configuration:
    services = {}

    def __init__(self, config_file=CONFIG_FILE):
        if self.exists(config_file):
            config = yaml.load(open(CONFIG_FILE, 'r'))
            self.services = config.get('services')

    @staticmethod
    def exists(config_file=CONFIG_FILE):
        return isfile(config_file)


class Service:
    pass
