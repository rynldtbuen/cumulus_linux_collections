from ...utils import iterkeys_value
from ..config import BaseConfig


class Interface(BaseConfig):
    HAS_UNIQUE_KEY = True

    @classmethod
    def get_applied_config(cls, opinions):
        try:
            applied_config = opinions["interface"]
        except KeyError:
            return {}

        section = cls.SECTION
        config = {}

        for k, v in applied_config.items():
            try:
                section_config = v[section]
            except KeyError:
                continue
            config[k] = {section: section_config}

        return config

    @classmethod
    def from_nvue_config(cls, name, config):
        obj = cls(name=name)
        obj_keys = obj.keys
        new_config = {}
        for keys, value in iterkeys_value(config):
            ref = new_config
            for key in keys[:-1]:
                if key in obj_keys:
                    continue
                ref[key] = {}
                ref = ref[key]
            ref[keys[-1]] = value
        obj._set_config = new_config

        return obj
