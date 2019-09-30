import pprint

import requests
# from paho import mqtt

latest_named = "http://api.thingspeak.com/channels/1417/field/1/last.json"
latest_hex = "http://api.thingspeak.com/channels/1417/field/2/last.json"
full = "http://api.thingspeak.com/channels/1417/feed.json"

colours = {
    'red': '#FF0000',
    'green': '#008000',
    'blue': '#0000FF',
    'cyan': '#00FFFF',
    'white': '#FFFFFF',
    'oldlace': '#FDF5E6',
    'warmwhite': '#FDF5E6',
    'purple ': '#800080',
    'magenta ': '#FF00FF',
    'yellow': '#FFFF00',
    'orange': '#FFA500',
    'pink': '#FFC0CB'
}


class CheerlightsWrapper(object):
    def __init__(self):
        self.callbacks = []
        self.latest = None

    def subscribe(self, callback):
        self.callbacks.append(callback)

    def history(self):
        json = requests.get(full).json()
        hex_list = list(map(lambda entry: entry["field2"], json["feeds"]))
        self.set_latest(hex_list[-1:][0])
        return hex_list

    def check(self):
        hex = requests.get(latest_hex).json()["field2"]
        self.set_latest(hex)

    def set_latest(self, hex):
        if not self.latest or self.latest != hex:
            self.latest = hex
            for callback in self.callbacks:
                callback(hex)


def printy_callback(foo):
    print(foo)


if __name__ == '__main__':
    c = CheerlightsWrapper()
    c.subscribe(printy_callback)
    c.check()
    # pprint.pprint(c.history())
