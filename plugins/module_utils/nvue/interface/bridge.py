from ...utils import ungroup
from .base import Interface


class Bridge(Interface):
    MODULE_NAME = "bridge_interfaces"
    SECTION = "bridge"
    PARAM_KEYS = (
        "learning",
        "untagged",
        "access",
        "stp",
        "vlans",
    )

    @property
    def keys(self):
        return ("interface", self._name, "bridge", "domain")

    @classmethod
    def from_ansible_item_config(cls, params_config):
        config = {}
        for k in cls.PARAM_KEYS:
            v = params_config.get(k)
            if v is None:
                continue
            try:
                func = getattr(cls, f"_{k}")
            except AttributeError:
                if isinstance(v, int):
                    v = str(v)
                config[k] = v
            else:
                config.update(func(v))

        return cls(
            name=params_config.get("name"),
            config={params_config.get("domain"): config},
        )

    @staticmethod
    def _vlans(value):
        return {"vlan": {v: {} for v in ungroup(value)}}
