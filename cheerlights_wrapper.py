import pprint

import requests

latest_named = "http://api.thingspeak.com/channels/1417/field/1/last.json"
latest_hex = "http://api.thingspeak.com/channels/1417/field/2/last.json"
full = "http://api.thingspeak.com/channels/1417/feed.json"


class CheerlightsWrapper(object):
    def __init__(self):
        self.callbacks = []
        self.latest = None

    def subscribe(self, callback):
        self.callbacks.append(callback)

    def history(self):
        json = requests.get(full).json()
        hex_list = list(map(lambda entry: entry["field2"], json["feeds"]))
        self.set_latest(hex_list[-1:])
        return hex_list

    def check(self):
        hex = requests.get(latest_hex).json()["field2"]
        self.set_latest(hex)

    def set_latest(self, hex):
        if not self.latest or self.latest != hex:
            self.latest = hex
            for callback in self.callbacks:
                callback(hex)


if __name__ == '__main__':
    c = CheerlightsWrapper()
    c.subscribe(print)
    c.check()
    # pprint.pprint(c.history())
