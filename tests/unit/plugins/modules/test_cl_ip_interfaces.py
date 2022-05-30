import pytest

from ansible_collections.rynld.cumulus_linux.plugins.module_utils.utils import to_json
from ansible_collections.rynld.cumulus_linux.plugins.module_utils.nvue.interface.ip import (
    IP,
)
from .data.interface import ip


def _get_group_command(param):
    return param[0]


@pytest.fixture(params=ip.test_params_config, ids=_get_group_command)
def manager(request):
    mngr = IP.manager
    key, config = request.param
    mngr._create_objects_from_ansible_params_config(config)
    return key, mngr


def test_nvue_config(manager):
    key, mngr_obj = manager
    group_actual_results = getattr(ip, key)

    for method in ("set", "unset"):
        for _type in ("config", "commands"):

            expected_result = getattr(mngr_obj, f"get_{_type}")(method=method)
            actual_result = group_actual_results[f"{method}_{_type}"]

            assert expected_result == actual_result, to_json(
                {"expected": expected_result, "actual": actual_result}
            )


@pytest.mark.parametrize(
    "manager", ip.test_state_config, ids=_get_group_command, indirect=True
)
def test_state_config(manager):
    state, mngr_obj = manager
    state_actual_results = getattr(ip, state)

    if state == "overridden":
        mngr_obj._applied_config = ip.applied_config

    expected_config = getattr(mngr_obj, f"get_{state}_config")()
    actual_config = state_actual_results["config"]
    assert expected_config == actual_config, to_json(
        {"expected": expected_config, "actual": actual_config}
    )

    expected_commands = mngr_obj.get_commands(expected_config)
    actual_commands = state_actual_results["commands"]

    assert len(expected_commands) == len(actual_commands)

    for cmd in expected_commands:
        assert cmd in actual_commands, f"{cmd} not in {actual_commands}"
