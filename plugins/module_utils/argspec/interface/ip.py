argument_spec = {
    "config": {
        "type": "list",
        "elements": "dict",
        "options": {
            "name": {
                "type": "str",
                "required": True,
            },
            "vrf": {
                "type": "str",
            },
            "addresses": {
                "type": "list",
            },
            "vrr": {
                "type": "dict",
                "options": {
                    "enable": {
                        "type": "str",
                        "choices": ["on", "off"],
                    },
                    "addresses": {
                        "type": "list",
                    },
                    "mac-id": {
                        "type": "str",
                    },
                    "mac-address": {
                        "type": "str",
                    },
                    "state": {
                        "type": "str",
                        "choices": ["up", "down"],
                    },
                },
            },
            "vrrp": {
                "type": "dict",
                "options": {
                    "enable": {"type": "str", "choices": ["on", "off"]},
                    "virtual-routers": {
                        "type": "list",
                        "elements": "dict",
                        "options": {
                            "id": {
                                "type": "int",
                                "required": True,
                            },
                            "version": {
                                "type": "int",
                                "choices": [2, 3],
                            },
                            "priority": {
                                "type": "int",
                            },
                            "preempt": {
                                "type": "str",
                                "choices": ["on", "off", "auto"],
                            },
                            "advertisement-interval": {
                                "type": "int",
                            },
                            "addresses": {
                                "type": "list",
                            },
                        },
                    },
                },
            },
            "gateways": {
                "type": "list",
            },
            "ipv4": {
                "type": "dict",
                "options": {
                    "forward": {
                        "type": "str",
                        "choices": ["on", "off"],
                    },
                },
            },
            "ipv6": {
                "type": "dict",
                "options": {
                    "enable": {
                        "type": "str",
                        "choices": ["on", "off"],
                    },
                    "forward": {
                        "type": "str",
                        "choices": ["on", "off"],
                    },
                },
            },
            "igmp": {
                "type": "dict",
                "options": {
                    "enable": {
                        "type": "str",
                        "choices": ["on", "off"],
                    },
                    "version": {
                        "type": "int",
                    },
                    "query-interval": {"type": "int"},
                    "query-max-response-time": {
                        "type": "int",
                    },
                    "last-member-query-interval": {
                        "type": "int",
                    },
                    "static-groups": {
                        "type": "list",
                        "elements": "dict",
                        "options": {
                            "id": {
                                "type": "int",
                                "required": True,
                            },
                            "source-address": {
                                "type": "str",
                            },
                        },
                    },
                },
            },
        },
    },
    "state": {
        "type": "str",
        "choices": [
            "merged",
            "replaced",
            "overridden",
            "rendered",
            "gathered",
        ],
    },
    "save": {"type": "bool", "default": False},
    "detach_pending_config": {
        "type": "bool",
        "default": False,
    },
    "overwrite_all_files": {
        "type": "bool",
        "default": False,
    },
}
