#!/usr/bin/python
# Copyright: (c) 2020, Reynold Tabuena <rynldtbuen@gmail.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: cl_ip_interfaces
short_description: interface IP resource module
description: Configure NVIDIA Cumulus Linux IP interfaces using NVUE
version_added: 1.0.0
author: Reynold Tabuena (@rynldtbuen)
notes:
- Tested against NVIDIA Cumulus Linux VX 5.0
options:
    config:
        description: list of configuration
        type: list
        elements: dict
        suboptions:
            name:
                description: Name of the interface
                type: str
                required: true
            vrf:
                description: VRF name instance
                type: str
            addresses:
                description: IPv4 or IPv6 addresses with prefix
                type: list
            vrr:
                description: VRR configuration
                type: dict
                suboptions:
                    enable:
                        description: enable or disable IPv6 feature
                        type: str
                        choices: [on, off]
                    addresses:
                        description: IPv4 or IPv6 addresses with prefix
                        type: list
                    mac-id:
                        description: Override anycast-id
                        type: str
                    mac-address:
                        description: Override anycast-mac
                        type: str
                    state:
                        description: The state of the interface
                        type: str
                        choices:
                        - up
                        - down
            vrrp:
                description: VRRP Configuration
                type: dict
                suboptions:
                    enable:
                        description: enable or disable the feature
                        type: str
                        choices:
                        - on
                        - off
                    virtual-routers:
                        description: Group of virtual gateways implemented with VRRP
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: Virtual-router ID
                                type: int
                                required: true
                            version:
                                description: Protocol version
                                type: int
                                choices:
                                - 2
                                - 3
                            priority:
                                description: set the interface priority
                                type: int
                            preempt:
                                description: Enable preemption
                                type: str
                                choices:
                                - on
                                - off
                                - auto
                            advertisement-interval:
                                description:
                                - Sets the interval between successive VRRP advertisements
                                - Represented in units of milliseconds
                                type: int
                            addresses:
                                description: IPv4 or IPv6 Virtual addresses
                                type: list
            gateways:
                description: IPv4 or IPv6 address
            ipv4:
                description: IPv4 configuration
                type: dict
                suboptions:
                    forward:
                        description: Enable or disable forwarding
                        type: str
                        choices:
                        - on
                        - off
            ipv6:
                description: IPv6 configuration
                type: dict
                suboptions:
                    enable:
                        description: Enable or disable feature
                        type: str
                        choices:
                        - on
                        - off
                    forward:
                        description: Enable or disable forwarding
                        type: str
                        choices:
                        - on
                        - off
            igmp:
                description: IGMP configuration
                type: dict
                suboptions:
                    enable:
                        description: Enable or disable feature
                    version:
                        description: Protocol version
                    query-interval:
                        description: Query interval, in seconds
                        type: int
                    query-max-response-time:
                        description: Max query response time, in seconds
                        type: int
                    last-member-query-interval:
                        description: Last member query interval
                        type: int
                    static-groups:
                        description: static mutlicast mroutes
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: Group ID
                                type: int
                            source-address:
                                description: Multicast mroute source
    state:                      type: str
        description: The state of the configuration
        type: str
        choices:
        - merged
        - replaced
        - overridden
        - rendered
        - gathered
        default: merged
    save:
        description: this will apply the pending config to running config and write it to startup config
        type: bool
        default: false
    as_nvue_config:
        description: if true, return the state diff config as NVUE config format else NVUE commands
        type: bool
        default: false
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.rynld.cumulus_linux.plugins.module_utils.nvue.interface.ip import (
    IP,
)
from ansible_collections.rynld.cumulus_linux.plugins.module_utils.argspec.interface import (
    ip,
)


if __name__ == "__main__":
    required_if = [
        ("state", "merged", ("config",)),
        ("state", "replaced", ("config",)),
        ("state", "overridden", ("config",)),
        ("state", "rendered", ("config",)),
    ]
    module = AnsibleModule(
        argument_spec=ip.argument_spec,
        required_if=required_if,
        supports_check_mode=True,
    )
    IP.manager.execute_module(module)
