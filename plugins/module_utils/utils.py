# Copyright: (c) 2020, Reynold Tabuena <rynldtbuen@gmail.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import json
import re
from itertools import groupby, count


def run_command(module, command=None, strict=True):
    def wrapper(command, strict=True):
        rc, stdout, stderr = run_cmd(command)
        if not strict:
            return rc, stdout, stderr
        if stderr or rc:
            module.fail_json(msg=stderr)
        return stdout

    run_cmd = module.run_command
    if command is None:
        return wrapper
    return wrapper(command, strict)


def to_json(value):
    return json.dumps(value, indent=2)


def iterkeys_value(iterables, _keys=None):
    """
    Extract dictionary into a list of keys and its value.

    Example:
        {"a": {"b": 2}, "c": 3} -> [(("a", "b"), 2), ((b,), 2)]
    """
    try:
        iter_items = iterables.items()
    except AttributeError:
        iter_items = iterables

    if _keys is None:
        _keys = []
    _keys_pop = _keys.pop

    for k, v in iter_items:
        try:
            items = v.items()
        except AttributeError:
            try:
                yield (*_keys, k), v
            except TypeError:
                yield (k,), v
        else:
            if not items:
                yield (*_keys, k), v
            else:
                _keys.append(k)
                yield from iterkeys_value(items, _keys=_keys)
                _keys_pop()


def string_value(key, value, ref):
    ref[key] = value[0]
    return True, None


def enable_config(key, value, ref):
    if not value:
        ref[key] = {"enable": "on"}
        return True, None
    ref[key] = {}
    ref = ref[key]
    return False, ref


def _iter_normalized_argspec(config, normalized_argspec_class=None):
    if normalized_argspec_class is None:
        return iter(config.items())
    for k, v in config.items():
        if v is None:
            continue
        try:
            normalized = getattr(normalized_argspec_class, k)
        except AttributeError:
            yield k, v
        else:
            yield normalized(v)


def _get_prefix_id(value):
    c = re.compile(r"(?P<name>\S+|)(?<!(\d|-|\.))(?P<zero>0{1,}|)(?P<id>\d+.*)")
    m = re.match(c, value)

    if m is None:
        return value, None

    name = m.group("name")

    if not name:
        name = ""
    else:
        name += m.group("zero")

    return name, int(m.group("id"))


def _unpack_range(value, prefix_name=None):
    start, end = value.split("-")
    try:
        int_start = int(start)
    except ValueError:
        _prefix_name, int_start = _get_prefix_id(start)
    else:
        _prefix_name = ""

    if not prefix_name:
        prefix_name = _prefix_name
    int_end = int(end)
    if int_start > int_end:
        raise ValueError(f"invalid range format: '{value}'")
    for item in range(int_start, int_end + 1):
        yield prefix_name, item


def _unpack_glob_range(iterables):
    prefix_name = ""
    for it in iterables:
        if "-" in it:
            _iter = _unpack_range(it, prefix_name)
        else:
            _iter = iter([_get_prefix_id(it)])

        for item in _iter:
            _prefix_name = item[0]
            if _prefix_name:
                yield _prefix_name, item[1]
            else:
                yield prefix_name, item[1]
            prefix_name = _prefix_name


def _iter_ungroup_raw_data(iterables):
    for it in iterables:
        if not it:
            continue

        it_split = it.split(",")
        if len(it_split) < 2:
            if "-" in it:
                yield from _unpack_range(it)
            else:
                yield _get_prefix_id(it)
        else:
            yield from _unpack_glob_range(it_split)


class ungroup:
    __slots__ = ("_raw_data",)

    def __init__(self, iterables=None, delimeter=None):
        if iterables is None:
            iterables = []
        raw_data = set()

        if delimeter is None:
            delimeter = " "

        try:
            iterables_split = iterables.split(delimeter)
        except AttributeError:
            if isinstance(iterables, (ungroup, group)):
                _raw_data = iterables._raw_data
            else:
                _raw_data = _iter_ungroup_raw_data(iterables)
        else:
            _raw_data = _iter_ungroup_raw_data(iterables_split)

        raw_data.update(_raw_data)
        self._raw_data = raw_data

    def __contains__(self, value):
        raw_value = _get_prefix_id(value)
        return raw_value in self._raw_data

    def __bool__(self):
        return bool(self._raw_data)

    def __iter__(self):
        for name, _id in sorted(self._raw_data):
            if _id is None:
                yield name
            else:
                yield f"{name}{_id}"

    def __repr__(self):
        return f"<ungroup: {list(self)}>"

    def __add__(self, other):
        if not isinstance(other, ungroup):
            raise NotImplementedError(f"{type(other)}")
        new = ungroup()
        new._raw_data = self._raw_data.union(other._raw_data)
        return new

    def __sub__(self, other):
        if not isinstance(other, ungroup):
            raise NotImplementedError(f"{type(other)}")
        new = ungroup()
        new._raw_data = self._raw_data - other._raw_data
        return new

    def __iadd__(self, value):
        add_item = self._raw_data.add
        for item in _iter_ungroup_raw_data(self._checkedval(value)):
            add_item(item)
        return self

    def __isub__(self, value):
        remove_item = self._raw_data.remove
        for item in _iter_ungroup_raw_data(self._checkedval(value)):
            try:
                remove_item(item)
            except KeyError as e:
                e.args = (f"{item[0]}{item[1]}",)
                raise

        return self

    def update(self, other):
        try:
            other_raw_ungrouped = other._raw_data
        except AttributeError:
            other_raw_ungrouped = _iter_ungroup_raw_data(self._checkedval(other))
        self._raw_data.update(other_raw_ungrouped)

    def clear(self):
        self._raw_data.clear()

    def copy(self):
        new = ungroup()
        new._raw_data = self._raw_data.copy()
        return new

    def _checkedval(self, value):
        try:
            return value.split(" ")
        except AttributeError:
            msg = f"expect str type object argument, fgot '{type(value)}'"
            raise NotImplementedError(msg) from None


class group:
    __slots__ = "_raw_data"

    def __init__(self, *args):
        self._raw_data = ungroup(*args)._raw_data

    def __iter__(self):
        for item in self._iter_grouped():
            try:
                yield "".join(item)
            except TypeError:
                yield item[0]

    def join(self, seperator=None, glob=False):
        def _glob():
            prefix_name = None
            for name, range_id in self._iter_grouped():
                if range_id is None:
                    yield name
                    continue
                if prefix_name == name:
                    yield range_id
                else:
                    yield f"{name}{range_id}"
                    prefix_name = name

        if seperator is None:
            seperator = ","

        if not glob:
            return f"{seperator}".join(self)
        return f"{seperator}".join(_glob())

    def _iter_grouped(self):
        def _key(_id, _count=count()):
            next_c = next(_count)
            try:
                return _id - next_c
            except TypeError:
                return next_c

        grouped = groupby(sorted(self._raw_data), key=lambda x: x[0])
        for prefix_name, v in grouped:
            for _, ids in groupby((i[-1] for i in v), key=_key):
                start = next(ids)
                if start is None:
                    print("NO")
                    yield prefix_name, None
                else:
                    item = None
                    # consume all item in generator to get the last item of ids
                    for item in ids:
                        pass
                    if item is None:
                        yield prefix_name, str(start)
                    else:
                        yield prefix_name, f"{start}-{item}"

    def __repr__(self):
        return f"<group: {list(self)}>"
