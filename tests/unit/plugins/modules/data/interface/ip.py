test_params_config = (
    (
        "address",
        [
            {"name": "swp1", "addresses": ["192.168.0.1/24", "::1"]},
            {"name": "swp2", "addresses": ["192.168.0.1/24", "::1"]},
        ],
    ),
    (
        "ipv4_ipv6",
        [
            {"name": "swp1", "ipv6": {"enable": "on", "forward": "on"}},
            {"name": "swp2", "ipv4": {"forward": "off"}},
        ],
    ),
    (
        "vrf",
        [
            {"name": "swp1", "vrf": "BLUE"},
            {"name": "swp2", "vrf": "RED"},
        ],
    ),
    (
        "gateway",
        [
            {"name": "swp1", "gateways": ["192.168.0.1/24"]},
            {"name": "swp2", "gateways": ["192.168.0.1/24"]},
        ],
    ),
    (
        "vrr",
        [
            {"name": "swp1", "vrr": {"enable": "on", "addresses": ["192.168.0.1/24"]}},
            {"name": "swp2", "vrr": {"enable": "on", "addresses": ["192.168.0.1/24"]}},
        ],
    ),
    (
        "vrrp",
        [
            {
                "name": "swp1",
                "vrrp": {
                    "virtual-routers": [
                        {"id": 1, "addresses": ["192.168.1.1/24"], "preempt": "on"},
                        {"id": 2, "addresses": ["192.168.2.1/24"], "priority": 255},
                    ]
                },
            },
            {
                "name": "swp2",
                "vrrp": {
                    "virtual-routers": [
                        {"id": 1, "addresses": ["192.168.1.1/24"], "preempt": "on"},
                        {"id": 2, "addresses": ["192.168.2.1/24"], "priority": 255},
                    ]
                },
            },
        ],
    ),
)


vrrp = {
    "set_config": {
        "set": {
            "interface": {
                "swp1": {
                    "ip": {
                        "vrrp": {
                            "virtual-router": {
                                "1": {
                                    "address": {
                                        "192.168.1.1/24": {},
                                    },
                                    "preempt": "on",
                                },
                                "2": {
                                    "address": {
                                        "192.168.2.1/24": {},
                                    },
                                    "priority": "255",
                                },
                            }
                        },
                    },
                },
                "swp2": {
                    "ip": {
                        "vrrp": {
                            "virtual-router": {
                                "1": {
                                    "address": {
                                        "192.168.1.1/24": {},
                                    },
                                    "preempt": "on",
                                },
                                "2": {
                                    "address": {
                                        "192.168.2.1/24": {},
                                    },
                                    "priority": "255",
                                },
                            }
                        },
                    },
                },
            },
        },
    },
    "unset_config": {
        "unset": {
            "interface": {
                "swp1": {
                    "ip": {
                        "vrrp": {
                            "virtual-router": {
                                "1": {
                                    "address": {
                                        "192.168.1.1/24": None,
                                    },
                                    "preempt": None,
                                },
                                "2": {
                                    "address": {
                                        "192.168.2.1/24": None,
                                    },
                                    "priority": None,
                                },
                            }
                        },
                    },
                },
                "swp2": {
                    "ip": {
                        "vrrp": {
                            "virtual-router": {
                                "1": {
                                    "address": {
                                        "192.168.1.1/24": None,
                                    },
                                    "preempt": None,
                                },
                                "2": {
                                    "address": {
                                        "192.168.2.1/24": None,
                                    },
                                    "priority": None,
                                },
                            }
                        },
                    },
                },
            },
        },
    },
    "set_commands": [
        "nv set interface swp1 ip vrrp virtual-router 1 address 192.168.1.1/24",
        "nv set interface swp1 ip vrrp virtual-router 1 preempt on",
        "nv set interface swp1 ip vrrp virtual-router 2 address 192.168.2.1/24",
        "nv set interface swp1 ip vrrp virtual-router 2 priority 255",
        "nv set interface swp2 ip vrrp virtual-router 1 address 192.168.1.1/24",
        "nv set interface swp2 ip vrrp virtual-router 1 preempt on",
        "nv set interface swp2 ip vrrp virtual-router 2 address 192.168.2.1/24",
        "nv set interface swp2 ip vrrp virtual-router 2 priority 255",
    ],
    "unset_commands": [
        "nv unset interface swp1 ip vrrp virtual-router 1 address 192.168.1.1/24",
        "nv unset interface swp1 ip vrrp virtual-router 1 preempt",
        "nv unset interface swp1 ip vrrp virtual-router 2 address 192.168.2.1/24",
        "nv unset interface swp1 ip vrrp virtual-router 2 priority",
        "nv unset interface swp2 ip vrrp virtual-router 1 address 192.168.1.1/24",
        "nv unset interface swp2 ip vrrp virtual-router 1 preempt",
        "nv unset interface swp2 ip vrrp virtual-router 2 address 192.168.2.1/24",
        "nv unset interface swp2 ip vrrp virtual-router 2 priority",
    ],
}


vrr = {
    "set_config": {
        "set": {
            "interface": {
                "swp1": {
                    "ip": {
                        "vrr": {
                            "enable": "on",
                            "address": {
                                "192.168.0.1/24": {},
                            },
                        },
                    },
                },
                "swp2": {
                    "ip": {
                        "vrr": {
                            "enable": "on",
                            "address": {
                                "192.168.0.1/24": {},
                            },
                        },
                    },
                },
            },
        },
    },
    "unset_config": {
        "unset": {
            "interface": {
                "swp1": {
                    "ip": {
                        "vrr": {
                            "enable": None,
                            "address": {
                                "192.168.0.1/24": None,
                            },
                        },
                    },
                },
                "swp2": {
                    "ip": {
                        "vrr": {
                            "enable": None,
                            "address": {
                                "192.168.0.1/24": None,
                            },
                        },
                    },
                },
            },
        },
    },
    "set_commands": [
        "nv set interface swp1 ip vrr enable on",
        "nv set interface swp1 ip vrr address 192.168.0.1/24",
        "nv set interface swp2 ip vrr enable on",
        "nv set interface swp2 ip vrr address 192.168.0.1/24",
    ],
    "unset_commands": [
        "nv unset interface swp1 ip vrr enable",
        "nv unset interface swp1 ip vrr address 192.168.0.1/24",
        "nv unset interface swp2 ip vrr enable",
        "nv unset interface swp2 ip vrr address 192.168.0.1/24",
    ],
}

gateway = {
    "set_config": {
        "set": {
            "interface": {
                "swp1": {
                    "ip": {
                        "gateway": {
                            "192.168.0.1/24": {},
                        },
                    },
                },
                "swp2": {
                    "ip": {
                        "gateway": {
                            "192.168.0.1/24": {},
                        },
                    },
                },
            },
        }
    },
    "unset_config": {
        "unset": {
            "interface": {
                "swp1": {
                    "ip": {
                        "gateway": {
                            "192.168.0.1/24": None,
                        },
                    },
                },
                "swp2": {
                    "ip": {
                        "gateway": {
                            "192.168.0.1/24": None,
                        },
                    },
                },
            },
        },
    },
    "set_commands": [
        "nv set interface swp1 ip gateway 192.168.0.1/24",
        "nv set interface swp2 ip gateway 192.168.0.1/24",
    ],
    "unset_commands": [
        "nv unset interface swp1 ip gateway 192.168.0.1/24",
        "nv unset interface swp2 ip gateway 192.168.0.1/24",
    ],
}

vrf = {
    "set_config": {
        "set": {
            "interface": {
                "swp1": {
                    "ip": {
                        "vrf": "BLUE",
                    },
                },
                "swp2": {
                    "ip": {
                        "vrf": "RED",
                    },
                },
            }
        }
    },
    "unset_config": {
        "unset": {
            "interface": {
                "swp1": {
                    "ip": {
                        "vrf": None,
                    },
                },
                "swp2": {
                    "ip": {
                        "vrf": None,
                    },
                },
            }
        }
    },
    "set_commands": [
        "nv set interface swp1 ip vrf BLUE",
        "nv set interface swp2 ip vrf RED",
    ],
    "unset_commands": [
        "nv unset interface swp1 ip vrf",
        "nv unset interface swp2 ip vrf",
    ],
}

ipv4_ipv6 = {
    "set_config": {
        "set": {
            "interface": {
                "swp1": {
                    "ip": {
                        "ipv6": {
                            "enable": "on",
                            "forward": "on",
                        }
                    },
                },
                "swp2": {
                    "ip": {
                        "ipv4": {
                            "forward": "off",
                        },
                    },
                },
            }
        }
    },
    "unset_config": {
        "unset": {
            "interface": {
                "swp1": {
                    "ip": {
                        "ipv6": {
                            "enable": None,
                            "forward": None,
                        }
                    },
                },
                "swp2": {
                    "ip": {
                        "ipv4": {
                            "forward": None,
                        },
                    },
                },
            }
        }
    },
    "set_commands": [
        "nv set interface swp1 ip ipv6 enable on",
        "nv set interface swp1 ip ipv6 forward on",
        "nv set interface swp2 ip ipv4 forward off",
    ],
    "unset_commands": [
        "nv unset interface swp1 ip ipv6 enable",
        "nv unset interface swp1 ip ipv6 forward",
        "nv unset interface swp2 ip ipv4 forward",
    ],
}

address = {
    "set_config": {
        "set": {
            "interface": {
                "swp1": {
                    "ip": {
                        "address": {
                            "192.168.0.1/24": {},
                            "::1": {},
                        }
                    }
                },
                "swp2": {
                    "ip": {
                        "address": {
                            "192.168.0.1/24": {},
                            "::1": {},
                        }
                    }
                },
            }
        }
    },
    "unset_config": {
        "unset": {
            "interface": {
                "swp1": {
                    "ip": {
                        "address": {
                            "192.168.0.1/24": None,
                            "::1": None,
                        }
                    }
                },
                "swp2": {
                    "ip": {
                        "address": {
                            "192.168.0.1/24": None,
                            "::1": None,
                        }
                    }
                },
            }
        }
    },
    "set_commands": [
        "nv set interface swp1 ip address 192.168.0.1/24",
        "nv set interface swp1 ip address ::1",
        "nv set interface swp2 ip address 192.168.0.1/24",
        "nv set interface swp2 ip address ::1",
    ],
    "unset_commands": [
        "nv unset interface swp1 ip address 192.168.0.1/24",
        "nv unset interface swp1 ip address ::1",
        "nv unset interface swp2 ip address 192.168.0.1/24",
        "nv unset interface swp2 ip address ::1",
    ],
}

test_state_config = (
    (
        "merged",
        [
            {
                "name": "swp1",
                "addresses": ["192.168.1.1/24"],
                "vrf": "RED",
            },
            {
                "name": "swp2",
                "addresses": ["192.168.1.1/24"],
                "vrf": "BLUE",
            },
        ],
    ),
    (
        "replaced",
        [
            {
                "name": "swp1",
                "addresses": ["192.168.1.1/24"],
                "vrf": "RED",
            },
            {
                "name": "swp2",
                "addresses": ["192.168.1.1/24"],
                "vrf": "BLUE",
            },
        ],
    ),
    (
        "rendered",
        [
            {
                "name": "swp1",
                "addresses": ["192.168.1.1/24", "192.168.1.2/24"],
                "vrf": "RED",
            },
            {
                "name": "swp2",
                "addresses": ["192.168.1.1/24"],
                "vrf": "BLUE",
            },
        ],
    ),
    (
        "overridden",
        [
            {
                "name": "swp1",
                "addresses": ["192.168.1.1/24", "192.168.1.2/24"],
                "vrf": "RED",
            },
            {
                "name": "swp2",
                "addresses": ["192.168.1.1/24"],
                "vrf": "BLUE",
            },
        ],
    ),
)

applied_config = {
    "interface": {
        "swp1": {
            "bridge": {
                "domain": {
                    "br_default": {},
                },
            },
            "ip": {
                "address": {
                    "192.168.100.1/24": {},
                },
            },
            "link": {
                "state": {
                    "up": {},
                },
            },
            "type": "swp",
        },
        "swp10": {
            "bridge": {
                "domain": {
                    "br_default": {},
                },
            },
            "ip": {
                "address": {
                    "192.168.0.1/24": {},
                },
            },
            "link": {
                "state": {
                    "up": {},
                },
            },
            "type": "swp",
        },
        "swp11": {
            "bridge": {
                "domain": {
                    "br_default": {},
                },
            },
            "ip": {
                "address": {
                    "192.168.1.1/24": {},
                    "192.168.1.2/24": {},
                },
            },
            "link": {
                "state": {
                    "up": {},
                },
            },
            "type": "swp",
        },
    },
    "system": {"hostname": "leaf1"},
}

overridden = {
    "config": {
        "unset": {
            "interface": {
                "swp1": {
                    "ip": None,
                },
                "swp2": {
                    "ip": None,
                },
                "swp10": {
                    "ip": None,
                },
                "swp11": {
                    "ip": None,
                },
            }
        },
        "set": {
            "interface": {
                "swp1": {
                    "ip": {
                        "address": {
                            "192.168.1.1/24": {},
                            "192.168.1.2/24": {},
                        },
                        "vrf": "RED",
                    }
                },
                "swp2": {
                    "ip": {
                        "address": {
                            "192.168.1.1/24": {},
                        },
                        "vrf": "BLUE",
                    }
                },
            },
        },
    },
    "commands": [
        "nv unset interface swp1 ip",
        "nv unset interface swp2 ip",
        "nv unset interface swp10 ip",
        "nv unset interface swp11 ip",
        "nv set interface swp1 ip address 192.168.1.1/24",
        "nv set interface swp1 ip address 192.168.1.2/24",
        "nv set interface swp1 ip vrf RED",
        "nv set interface swp2 ip address 192.168.1.1/24",
        "nv set interface swp2 ip vrf BLUE",
    ],
}

rendered = {
    "config": {
        "set": {
            "interface": {
                "swp1": {
                    "ip": {
                        "address": {
                            "192.168.1.1/24": {},
                            "192.168.1.2/24": {},
                        },
                        "vrf": "RED",
                    }
                },
                "swp2": {
                    "ip": {
                        "address": {
                            "192.168.1.1/24": {},
                        },
                        "vrf": "BLUE",
                    }
                },
            }
        }
    },
    "commands": [
        "nv set interface swp1 ip address 192.168.1.1/24",
        "nv set interface swp1 ip address 192.168.1.2/24",
        "nv set interface swp1 ip vrf RED",
        "nv set interface swp2 ip address 192.168.1.1/24",
        "nv set interface swp2 ip vrf BLUE",
    ],
}


merged = {
    "config": {
        "set": {
            "interface": {
                "swp1": {
                    "ip": {
                        "address": {
                            "192.168.1.1/24": {},
                        },
                        "vrf": "RED",
                    }
                },
                "swp2": {
                    "ip": {
                        "address": {
                            "192.168.1.1/24": {},
                        },
                        "vrf": "BLUE",
                    }
                },
            }
        }
    },
    "commands": [
        "nv set interface swp1 ip address 192.168.1.1/24",
        "nv set interface swp1 ip vrf RED",
        "nv set interface swp2 ip address 192.168.1.1/24",
        "nv set interface swp2 ip vrf BLUE",
    ],
}


replaced = {
    "config": {
        "unset": {
            "interface": {
                "swp1": {
                    "ip": None,
                },
                "swp2": {
                    "ip": None,
                },
            },
        },
        "set": {
            "interface": {
                "swp1": {
                    "ip": {
                        "address": {
                            "192.168.1.1/24": {},
                        },
                        "vrf": "RED",
                    }
                },
                "swp2": {
                    "ip": {
                        "address": {
                            "192.168.1.1/24": {},
                        },
                        "vrf": "BLUE",
                    }
                },
            }
        },
    },
    "commands": [
        "nv unset interface swp1 ip",
        "nv unset interface swp2 ip",
        "nv set interface swp1 ip address 192.168.1.1/24",
        "nv set interface swp1 ip vrf RED",
        "nv set interface swp2 ip address 192.168.1.1/24",
        "nv set interface swp2 ip vrf BLUE",
    ],
}
