import json
import sys
from typing import Mapping, MutableSequence

from .main import main

if len(sys.argv) < 2:
    print("provide arguement")
    exit()

bot = sys.argv[1]


class AttrDict:
    """A read-only façade for navigating a JSON-like object
    using attribute notation
    """

    def __init__(self, mapping):
        self._data = dict(mapping)

    def __getattr__(self, name):
        if hasattr(self._data, name):
            return getattr(self._data, name)
        else:
            try:
                return AttrDict.build(self._data[name])

            except KeyError:
                raise AttributeError(f"json object has no attribute {name}")

    @classmethod
    def build(cls, obj):
        if isinstance(obj, Mapping):
            return cls(obj)
        elif isinstance(obj, MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


config_dict = json.loads(open("moddy/config.json").read())
if bot not in config_dict:
    print("not a valid bot")
    exit()

config_dict[bot]["common"] = config_dict["common"]
bot_config = AttrDict(config_dict[bot])

main(bot_config)
