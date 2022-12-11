import json

"""
Here will be stored different tools who will help to get some common values or operation
"""


def val_key(key, file="config.json"):
    with open(file, "r") as config:
        return json.load(config)[key]


def save_value(key, value, file="config.json"):
    with open(file, "r+") as config:
        data = json.load(config)
        data["plex"][key] = value
        config.seek(0)
        json.dump(data, config, indent=4)
        config.truncate()
