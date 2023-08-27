#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/interfaces.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import (
    module_dependency_error,
    MODULE_EXCEPTIONS,
)

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import (
        profiler,
    )
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import (
        diff_remove_empty,
    )
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import (
        OPN_MOD_ARGS,
        STATE_ONLY_MOD_ARG,
        RELOAD_MOD_ARG,
    )
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.interface import (
        Interface,
    )

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = "https://opnsense.ansibleguy.net/en/latest/modules/interface.html"
EXAMPLES = "https://opnsense.ansibleguy.net/en/latest/modules/interface.html"


def run_module():
    module_args = dict(
        interface=dict(type="str", required=True, aliases=["int"]),
        name=dict(type="str", required=False, aliases=["id"]),
        description=dict(
            type="str",
            required=False,
            aliases=["desc"],
            default="",
            description="Enter a description (name) for the interface here",
        ),
        enable=dict(type="bool", required=False, default=False),
        lock=dict(type="bool", required=False, default=False),
        block_bogon_networks=dict(type="bool", required=False, default=False),
        block_private_networks=dict(type="bool", required=False, default=False),
        promiscuous_mode=dict(type="bool", required=False, default=False),
        mtu=dict(type="int", required=False, default=1500),
        mac_address=dict(type="str", required=False, default=""),
        type4=dict(
            type="str",
            required=False,
            default="none",
            description="IPv4 Configuration Type",
        ),
        ip4=dict(
            type="str",
            required=False,
            default="",
        ),
        mask4=dict(
            type="str",
            required=False,
            default="",
        ),
        gw4=dict(
            type="str",
            required=False,
            default="",
        ),
        type6=dict(
            type="str",
            required=False,
            default="none",
            description="IPv6 Configuration Type",
        ),
        ip6=dict(
            type="str",
            required=False,
            default="",
        ),
        mask6=dict(
            type="str",
            required=False,
            default="",
        ),
        gw6=dict(
            type="str",
            required=False,
            default="",
        ),
        **RELOAD_MOD_ARG,
        **STATE_ONLY_MOD_ARG,
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
        diff={
            "before": {},
            "after": {},
        },
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    interface = Interface(module=module, result=result)

    def process():
        interface.check()
        interface.process()
        if result["changed"] and module.params["reload"]:
            interface.reload()

    if PROFILE or module.params["debug"]:
        profiler(check=process, log_file="interface.log")
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    interface.s.close()
    result["diff"] = diff_remove_empty(result["diff"])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
