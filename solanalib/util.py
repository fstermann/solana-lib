from typing import List


class SafeDict(dict):
    def __getitem__(self, key):
        try:
            value = dict.__getitem__(self, key)
            if isinstance(value, dict):
                value = type(self)(value)
        except KeyError:
            value = type(self)()
        return value


def make_list_batches(full_list: List, batch_size: int):
    for i in range(0, len(full_list), batch_size):
        yield full_list[i : i + batch_size]
