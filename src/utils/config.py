import json


class _MetaConfig(type):
    def __getattr__(cls, name):
        with open("config.json", "r") as f:
            cls._config = json.load(f)
        return cls._config.get(name)


class Config(metaclass=_MetaConfig):
    pass
