# this file handles loading x86.json

import json

class Desc:
    def __init__(self, path: str):
        desc = None
        with open(path, "r") as f:
            desc = json.load(f)

        print(desc)
