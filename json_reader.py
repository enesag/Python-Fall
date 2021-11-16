import json


def read(filePath):
    with open(filePath) as file:
        return json.load(file)
