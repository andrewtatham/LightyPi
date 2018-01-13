import pprint
import random

from phue import Bridge


class HueWrapper(object):
    def __init__(self, bridge_ip='192.168.0.20', light_name='DEATH STAR'):

        self.light_name = light_name
        self.bridge_ip = bridge_ip
        self.b = None
        self.light = None

    def connect(self):
        self.b = Bridge(self.bridge_ip)
        self.b.connect()
        for l in self.b.lights:
            text = l.name
            if l.name == self.light_name:
                text += " *"
                self.light = l
            print(text)
        if self.light:
            print("connected")
            pprint.pprint(self.light.__dict__)

    def on(self):
        if self.light:
            self.light.on = True

    def colour_temperature(self, temp):
        # (white only) 154 is the coolest, 500 is the warmest
        if self.light:
            self.light.ct = temp

    def xy(self, x, y):
        #  co-ordinates in CIE 1931 space
        if self.light:
            self.light.xy = (x, y)

    def random_colour(self):
        if self.light:
            self.light.xy = [random.random(), random.random()]

    def hue(self, hue, sat):
        # hue' parameter has the range 0-65535 so represents approximately 182*degrees
        # sat is 0-255?
        if self.light:
            self.light.hue = hue
            self.light.sat = sat

    def brightness(self, bright):
        # // brightness between 0-254 (NB 0 is not off!)
        if self.light:
            self.light.bri = bright

    def colour_loop(self):
        if self.light:
            self.light.effect = "colorloop"

    def flash_once(self):
        if self.light:
            self.light.alert = "select"

    def flash_multiple(self):
        if self.light:
            self.light.alert = "lselect"

    def flash_off(self):
        if self.light:
            self.light.alert = None

    def off(self):
        if self.light:
            self.light.on = False

    @property
    def is_on(self):
        return self.light.on

    def set_hsv(self, h, s, v):
        if not self.light.on:
            self.on()
        h = int(h * 65535)
        s = int(s * 255)
        v = int(v * 255)
        print((h, s, v))
        self.light.hue = h
        self.light.sat = s
        self.light.bri = v

    def quick_transitions(self):
        if self.light:
            self.light.transitiontime = 0


if __name__ == '__main__':
    hue = HueWrapper()
    hue.connect()

    hue.on()
    hue.brightness(254)
    for _ in range(5):
        hue.random_colour()

    hue.colour_temperature(154)
    hue.colour_temperature(500)
    hue.colour_temperature(154)
    hue.colour_loop()
    hue.off()
