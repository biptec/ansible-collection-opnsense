from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Interface(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'assign': 'assignItem',
        'del': 'delItem',
        'set': 'setItem',
        'search': 'get',
    }
    API_KEY_PATH = 'interface.interface'
    API_MOD = 'interfaces'
    API_CONT = 'settings'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['interface', 'vlan', 'priority', 'description']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'name': 'if',
        'description': 'descr',

        '':'blockbogons',
        '':'blockpriv',
        '':'promisc',
        'mac_address':'spoofmac',

        'type4':'type',
        'ip4':'ipaddr',
        'mask4': 'subnet',
        'gw4': 'gateway',

        'type6':'type6',
        'ipv6':'ipaddrv6',
        'mask6': 'subnetv6',
        'gw6': 'gateway6',
    }
    FIELDS_TYPING = {
        'bool': ['enable', 'lock'],
        'select': ['type4', 'type6'],
        'int': ['mtu', 'mms'],
    }
    INT_VALIDATIONS = {
        'mtu': {'min': 576, 'max': 1500},
        'mask4': {'min': 1, 'max': 32},
        'mask6': {'min': 1, 'max': 128},
    }
    EXIST_ATTR = 'name'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.vlan = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['interface']):
                self.m.fail_json("You need to provide an 'interface' to create a vlan!")

            if is_unset(self.p['vlan']):
                self.m.fail_json("You need to provide a 'vlan' to create a vlan-interface!")

            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self._base_check()

    def update(self) -> None:
        self.b.update(enable_switch=False)
