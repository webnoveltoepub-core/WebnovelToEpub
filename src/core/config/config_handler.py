import json

# load json bytestream file as dict
class ConfigHandler:
    def __init__(self, config_bytes: bytes):
        self.__config: dict = json.loads(config_bytes.decode("utf-8"))

    def get_s_config(self) -> dict:
        return self.__config