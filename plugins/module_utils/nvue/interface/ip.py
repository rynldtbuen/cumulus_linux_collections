from .base import Interface


class IP(Interface):
    MODULE_NAME = "ip_interfaces"
    SECTION = "ip"
    PARAM_KEYS = (
        "vrf",
        "addresses",
        "vrr",
        "vrrp",
        "gateways",
        "ipv4",
        "ipv6",
        "igmp",
    )

    @property
    def keys(self):
        return ("interface", self._name, "ip")

    @classmethod
    def from_ansible_item_config(cls, item_config, **kwargs):
        config = {}
        for k in cls.PARAM_KEYS:
            v = item_config.get(k)
            if v is None:
                continue
            name = item_config.get("name")
            try:
                func = getattr(cls, f"_{k}")
            except AttributeError:
                config[k] = v
            else:
                config.update(func(v, name=name, **kwargs))

        return cls(name=name, config=config)

    @staticmethod
    def _addresses(value, **kwargs):
        if value is None:
            return {}
        return {"address": {i: {} for i in value}}

    @staticmethod
    def _gateways(value, **kwargs):
        return {"gateway": {i: {} for i in value}}

    @staticmethod
    def _state(value, **kwargs):
        return {"state": {value: {}}}

    @staticmethod
    def _vrr(value, **kwargs):
        config = {}
        for k, v in value.items():
            if v is not None:
                try:
                    func = getattr(IP, f"_{k}")
                except AttributeError:
                    config[k] = str(v)
                else:
                    config.update(func(v))

        return {"vrr": config}

    @staticmethod
    def _vrrp(value, **kwargs):
        keys = ("version", "priority", "preempt", "advertisement-interval")
        config = {}
        for item in value.get("virtual-routers", []):
            _id = str(item.get("id"))
            values = IP._addresses(item.get("addresses"))
            for key in keys:
                value = item.get(key)
                if value is not None:
                    values[key] = str(value)
            config[_id] = values

        return {"vrrp": {"virtual-router": config}}

    @staticmethod
    def _igmp(value, **kwargs):
        keys = (
            "enable",
            "version",
            "query-interval",
            "query-max-response-time",
            "last-member-query-interval",
        )

        new_config = {}

        for key in keys:
            val = value.get(key)
            if val is not None:
                new_config[key] = str(val)

        static_group = {
            str(sg.get("id")): {"source-address": sg.get("source-address")}
            for sg in value.get("static-groups", [])
        }
        if static_group:
            new_config["static-group"] = static_group

        return {"igmp": new_config}

    @staticmethod
    def _vrf(value, **kwargs):
        vrf = kwargs.get("applied_config")
        if vrf is not None:
            if kwargs.get("check"):
                raise IP.ConfigError(f"{kwargs.get('name')}: Vrf {value} not found")
        return {"vrf": value}
        # try:
        #
        # except KeyError:
        #     # For the sake of testing
        #     return {"vrf": value}
        # else:
        #     #
        #     if not kwargs.get("check"):
        #         return {"vrf": value}
        #     if vrf.get(value) is None:
        #         raise IP.ConfigError(f"{kwargs.get('name')}: Vrf {value} not found")
        #
        # return {"vrf": value}
