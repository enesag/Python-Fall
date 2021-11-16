import json
import random


class FortuneService:
    def __init__(self):
        with open("src/fortunes.json", encoding="utf-8") as fortunesFile:
            self.fortunes = json.load(fortunesFile)

    def getFortune(self):
        return random.choice(self.fortunes)
