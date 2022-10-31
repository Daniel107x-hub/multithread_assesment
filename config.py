import yaml
from yaml.loader import SafeLoader


class Configuration:
    def __init__(self, config_file: str) -> None:
        self._config = None
        with open(config_file) as file:
            self._config = yaml.load(file, Loader=SafeLoader)

    def get(self, property_name: str) -> object:
        return self._config[property_name] or None


configs = "config.yml"
configuration = Configuration(configs)
