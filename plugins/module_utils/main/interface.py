from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import (
    Session,
)
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import (
    validate_int_fields,
    is_unset,
    is_ip4,
    is_ip6,
)
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import (
    BaseModule,
)


class Interface(BaseModule):
    FIELD_ID = "interface"
    CMDS = {
        "add": "assignItem",
        "del": "delItem",
        "set": "setItem",
        "search": "get",
    }
    API_KEY_PATH = "interface.interface"
    API_MOD = "interfaces"
    API_CONT = "settings"
    API_CMD_REL = "reconfigure"
    FIELDS_CHANGE = [
        "interface",
        "description",
        "enable",
        "block_bogon_networks",
        "block_bogon_networks",
        "block_private_networks",
        "promiscuous_mode",
        "mac_address",
        "mtu",
        "lock",
        "type4",
        "ip4",
        "mask4",
        "gw4",
        "type6",
        "ip6",
        "mask6",
        "gw6",
    ]
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        "name": "id",
        "interface": "if",
        "description": "descr",
        "block_bogon_networks": "blockbogons",
        "block_private_networks": "blockpriv",
        "promiscuous_mode": "promisc",
        "mac_address": "spoofmac",
        #
        "type4": "type",
        "ip4": "ipaddr",
        "mask4": "subnet",
        "gw4": "gateway",
        #
        "type6": "type6",
        "ip6": "ipaddrv6",
        "mask6": "subnetv6",
        "gw6": "gatewayv6",
    }
    FIELDS_TYPING = {
        "bool": [
            "enable",
            "lock",
            "promiscuous_mode",
            "block_private_networks",
            "block_bogon_networks",
        ],
        "select": ["interface", "type4", "type6", "gw4", "gw6"],
        "int": ["mtu"],
    }
    INT_VALIDATIONS = {
        "mtu": {"min": 576, "max": 1500},
        "mask4": {"min": 1, "max": 32},
        "mask6": {"min": 1, "max": 128},
    }
    EXIST_ATTR = "interface"

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.interface = {}

    def check(self) -> None:
        if self.p["state"] == "present":
            if is_unset(self.p["interface"]):
                self.m.fail_json(
                    "You need to provide an 'interface' to assign a device!"
                )

            validate_int_fields(
                module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS
            )

            if self.p["type4"] == "static":
                if not is_ip4(self.p["ip4"]):
                    self.m.fail_json(
                        f"IPv4 '{self.p['ip4']}' is not a valid IPv4-address!"
                    )

            if self.p["type6"] == "static":
                if not is_ip6(self.p["ip6"]):
                    self.m.fail_json(
                        f"IPv6 '{self.p['ip6']}' is not a valid IPv6-address!"
                    )

        self._base_check()

    def update(self) -> None:
        self.b.update(enable_switch=False)
