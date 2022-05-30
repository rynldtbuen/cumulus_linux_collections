import json

try:
    from ruamel.yaml import YAML
except ImportError:
    import yaml
else:
    yaml = YAML()

from ..utils import iterkeys_value

NVUE_YAML_CONFIG_FILE = "/tmp/ansible_nvue_config.yaml"
NVUE_CONFIG_PATH = "/var/lib/nvue/config"
BASE_NVUE_REVISION_PATH = "/var/lib/nvue/meta"
ACTION_STATE = ("merged", "replaced", "overridden")


class ManagerDescriptor:
    def __get__(self, obj, objtype=None):
        if obj is not None:
            raise AttributeError(
                f"object 'Manager' can only be access through '{type(obj)}' object type"
            )
        try:
            return self._manager
        except AttributeError:
            manager = NVUEConfigManager(objtype)
            self._manager = manager
            return manager

    def __set__(self, obj, value):
        raise AttributeError("can't set attribute")

    def __delete__(self, obj, value):
        raise AttributeError("can't delete attribute")


def _build_dict_from_keys(keys, data):
    for key in keys:
        try:
            data = data[key]
        except KeyError:
            data[key] = {}
            data = data[key]
    return data


def _run_command(module, command=None):
    def wrapper(command, strict=True, **kwargs):
        if not strict:
            return run_cmd(command, **kwargs)
        rc, stdout, stderr = run_cmd(command, **kwargs)
        if stderr or rc:
            module.fail_json(msg=stderr)
        return stdout

    run_cmd = module.run_command
    if command is None:
        return wrapper
    return wrapper(command)


def _colored_diff(diff_output):
    diff = []
    diff_append = diff.append

    tuple_method = ("- set:", "- unset:")

    for item in diff_output.splitlines():
        if not item:
            continue

        if item in tuple_method:
            method = item

        if method == "- set:":
            diff_append(f"\033[92m{item}\033[0m")
        else:
            diff_append(f"\033[91m{item}\033[0m")

    return "\n".join(diff)
    # diff = []
    # diff_append = diff.append
    #
    # for cmd in diff_stdout.splitlines():
    #     if cmd.startswith("nv set"):
    #         diff_append(f"\033[92m{cmd}\033[0m")
    #     else:
    #         diff_append(f"\033[91m{cmd}\033[0m")
    #
    # return "\n".join(diff)


def _apply_config(module, run_command, overwrite_all_files=False):
    rc, out, err = run_command("/usr/bin/nv config apply --assume-no", strict=False)

    warning_is_overwrite_files = False
    for line in out.splitlines():
        if line.startswith("/etc"):
            warning_is_overwrite_files = True
            break

    if warning_is_overwrite_files:
        if not overwrite_all_files:
            _remove_current_pending(run_command)
            msg = (
                "NVUE need permision to overwrite files. "
                "Please use -vvv to see the files that will be overwritten "
                "and set the paramater 'overwrite_all_files' to 'yes'"
            )
            module.fail_json(msg=msg, stdout=out)
        run_command("/usr/bin/nv config apply", data="y")

    else:
        if err.startswith("apply_fail"):
            module.fail_json(msg=err)


def _remove_current_pending(run_command, rev_id=None):
    output = run_command("/usr/bin/nv config revision --current")
    current_revision = list(yaml.load(output))[0]
    run_command("nv config detach")
    run_command(f"/usr/bin/rm -f {BASE_NVUE_REVISION_PATH}/{current_revision}")


def _get_applied_config(run_command):
    run_command("/usr/bin/git checkout applied", strict=False, cwd=NVUE_CONFIG_PATH)
    nvue_json = run_command(f"/usr/bin/cat {NVUE_CONFIG_PATH}/nvue.json")
    if not nvue_json:
        return {}
    return json.loads(nvue_json)["opinions"]


class NVUEConfigManager:
    def __init__(self, klass):
        self._klass = klass
        self._objects = []
        self._applied_config = {}

    def execute_module(self, module):
        params = module.params
        run_command = _run_command(module)

        params_config = params["config"] or []
        applied_config = _get_applied_config(run_command)
        state = params["state"]
        check = state in ACTION_STATE

        try:
            self._create_objects_from_ansible_params_config(
                params_config,
                applied_config=applied_config,
                state=state,
                check=check,
            )
        except self._klass.ConfigError as e:
            module.fail_json(msg=str(e))

        # set applied config to be consume in generating configuration
        self._applied_config = applied_config

        # generate the NVUE config based on the state
        nvue_config = getattr(self, f"get_{state}_config")()

        results = {
            "changed": False,
            "commands": self.get_commands(nvue_config),
            "config": nvue_config,
        }

        # Early exit if nvue_config is empty or state is rendered or gathered
        if not nvue_config or not check:
            module.exit_json(**results)

        # Detach existing pending config else exit module
        existing_diff = run_command("/usr/bin/nv config diff")
        if existing_diff:
            if not params["detach_pending_config"]:
                msg = "There is an existing pending configuration"
                module.fail_json(msg=msg, pending=yaml.load(existing_diff))
            _remove_current_pending(run_command)

        # write NVUE yaml file to specified path and patch the config
        for method in nvue_config:
            with open(NVUE_YAML_CONFIG_FILE, "w") as file:
                yaml.dump([{method: nvue_config.get(method)}], file)
            run_command(f"/usr/bin/nv config patch {NVUE_YAML_CONFIG_FILE}")

        diff = run_command("/usr/bin/nv config diff")

        # Early exit if there is no diff in the config
        if not diff:
            module.exit_json(**results)

        colored_diff = _colored_diff(diff)

        results["changed"] = True

        if module._diff:
            results["diff"] = {"prepared": colored_diff}

        if not module.check_mode:
            _apply_config(module, run_command, params["overwrite_all_files"])
        else:
            _remove_current_pending(run_command)

        module.exit_json(**results)

    def get_commands(self, nvue_config=None, method="set"):
        if nvue_config is None:
            nvue_config = self.get_config(method=method)

        if not nvue_config:
            return []

        commands = []
        cmds_append = commands.append

        for keys, value in iterkeys_value(nvue_config):
            cmd = f"nv {' '.join(keys)}"
            if value:
                cmd += f" {value}"
            cmds_append(cmd)

        return commands

    def get_config(self, method="set"):
        config = {}

        for obj in self._objects:
            val = getattr(obj, f"_{method}_config")
            if not val:
                continue
            list_keys = list(obj.keys)
            last_key = list_keys.pop()
            ref = _build_dict_from_keys(list_keys, config)
            ref[last_key] = val

        if not config:
            return {}

        return {method: config}

    def get_merged_config(self):
        return self.get_config()

    def get_replaced_config(self):
        config = {"unset": {}, "set": {}}

        for obj in self._objects:
            list_keys = list(obj.keys)
            last_key = list_keys.pop()

            ref_unset = _build_dict_from_keys(list_keys, config["unset"])
            ref_unset[last_key] = None

            ref_set = _build_dict_from_keys(list_keys, config["set"])
            set_config = obj._set_config
            if not set_config:
                continue
            ref_set[last_key] = set_config

        return config

    def get_overridden_config(self):
        config = {"unset": {}, "set": {}}

        for obj in self._objects:
            list_keys = list(obj.keys)
            last_key = list_keys.pop()

            ref_unset = _build_dict_from_keys(list_keys, config["unset"])
            ref_unset[last_key] = None

            ref_set = _build_dict_from_keys(list_keys, config["set"])
            set_config = obj._set_config
            if not set_config:
                continue
            ref_set[last_key] = set_config

        klass = self._klass
        if self._klass.HAS_UNIQUE_KEY:
            for name in klass.get_applied_config(self._applied_config):
                obj = klass(name=name)
                list_keys = list(obj.keys)
                last_key = list_keys.pop()

                ref_unset = _build_dict_from_keys(list_keys, config["unset"])
                ref_unset[last_key] = None

        return config

    def get_rendered_config(self):
        return self.get_config()

    def get_gathered_config(self):
        applied_config = self._applied_config

        if not applied_config:
            return {}

        klass = self._klass
        if klass.HAS_UNIQUE_KEY:
            _applied_config = {}
            for name, config in klass.get_applied_config(applied_config).items():
                obj = klass.from_nvue_config(name=name, config=config)
                list_keys = list(obj.keys)
                last_key = list_keys.pop()

                ref = _build_dict_from_keys(list_keys, _applied_config)
                ref[last_key] = obj._set_config

            applied_config = _applied_config

        return {"set": applied_config}

    def _create_objects_from_ansible_params_config(self, params_config, **kwargs):
        klass = self._klass
        self._objects = [
            klass.from_ansible_item_config(item, **kwargs) for item in params_config
        ]
