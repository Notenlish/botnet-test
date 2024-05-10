import json


def get_config():
    with open("config.json", "r") as f:
        data = json.load(f)
    return data["ip"], data["port"], data["key"]
