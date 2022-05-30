from ..utils import iterkeys_value
from .manager import ManagerDescriptor


class BaseConfig:
    HAS_UNIQUE_KEY = False

    class ConfigError(Exception):
        pass

    def __init_subclass__(cls):
        setattr(cls, "manager", ManagerDescriptor())

    def __init__(self, **kwargs):
        self._set_config = kwargs.pop("config", {})
        for k, v in kwargs.items():
            setattr(self, f"_{k}", v)

    @property
    def _unset_config(self):
        config = {}

        for keys, value in iterkeys_value(self._set_config):
            ref = config

            for key in keys[:-1]:
                try:
                    ref = ref[key]
                except KeyError:
                    ref[key] = {}
                    ref = ref[key]

            ref.update({keys[-1]: None})

        return config
