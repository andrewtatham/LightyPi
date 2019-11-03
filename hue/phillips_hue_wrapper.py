import pprint
import random
import time

from phue import Bridge


class HueWrapper(object):
    def __init__(self, bridge_ip='192.168.1.73', light_configs=None):
        if not light_configs:
            light_configs = [
                {'name': 'Hue color spot 1', 'is_colour': True},
                {'name': 'Hue color spot 2', 'is_colour': True},
                {'name': 'Hue color spot 3', 'is_colour': True},
                {'name': 'DEATH STAR', 'is_colour': True},
                {'name': 'Right Colour Strip', 'is_colour': True},
                {'name': 'Right White Strip', 'is_colour': False},
                {'name': 'Left Colour Strip', 'is_colour': True},
                {'name': 'Left White Strip', 'is_colour': False},
            ]

        self.light_configs = light_configs
        self.bridge_ip = bridge_ip
        self.b = None
        self.lights = []

    def connect(self):
        self.b = Bridge(self.bridge_ip)
        self.b.connect()
        for actual_light in self.b.lights:
            name = actual_light.name
            for light_config in self.light_configs:
                if light_config['name'] == name:
                    name += " *"
                    actual_light.is_colour = light_config['is_colour']
                    self.lights.append(actual_light)
            print(name)
        if self.lights:
            print("connected")
            for actual_light in self.lights:
                pprint.pprint(actual_light.__dict__)

    def on(self):
        for light in self.lights:
            light.on = True

    def colour_temperature(self, temp):
        # (white only) 154 is the coolest, 500 is the warmest
        for light in self.lights:
            light.ct = temp

    def xy(self, x, y):
        #  co-ordinates in CIE 1931 space
        for light in self.lights:
            if light.is_colour:
                light.xy = (x, y)

    def random_colour(self):
        for light in self.lights:
            if light.is_colour:
                light.xy = [random.random(), random.random()]

    def hue(self, hue, sat):
        # hue' parameter has the range 0-65535 so represents approximately 182*degrees
        # sat is 0-254?
        for light in self.lights:
            light.hue = hue
            light.sat = sat

    def brightness(self, bright):
        # // brightness between 0-254 (NB 0 is not off!)
        for light in self.lights:
            light.bri = bright

    def colour_loop_off(self):
        for light in self.lights:
            if light.is_colour:
                light.effect = "none"

    def colour_loop_on(self):
        for light in self.lights:
            if light.is_colour:
                light.effect = "colorloop"

    def flash_once(self):
        for light in self.lights:
            light.alert = "select"

    def flash_multiple(self):
        for light in self.lights:
            light.alert = "lselect"

    def flash_off(self):
        for light in self.lights:
            light.alert = None

    def off(self):
        for light in self.lights:
            light.on = False

    @property
    def is_on(self):
        on = False
        for light in self.lights:
            on = on or light.on
        return on

    @property
    def is_off(self):
        return not self.is_on

    def set_hsv(self, h, s, v):
        h = int(h * 65535)
        s = int(s * 255)
        v = int(v * 255)
        print((h, s, v))
        for light in self.lights:
            if self.is_off:
                self.on()
            if light.is_colour:
                light.hue = h
                light.sat = s
                light.bri = v

    def quick_transitions(self):
        for light in self.lights:
            light.transitiontime = 0

    def sleep(self, seconds):
        time.sleep(seconds)

    def do_whatever(self):
        self.colour_loop_off()
        self.random_colour()
        # for light in self.lights:
        #     light.


if __name__ == '__main__':
    hue = HueWrapper()
    hue.connect()

    hue.on()
    hue.brightness(254)

    hue.colour_temperature(154)
    hue.sleep(3)
    hue.colour_temperature(500)
    hue.sleep(3)
    hue.colour_temperature(154)
    hue.sleep(3)

    for _ in range(5):
        hue.random_colour()
        hue.sleep(1)

    hue.colour_loop_on()
    hue.sleep(10)
    hue.colour_loop_off()
    hue.sleep(10)
    hue.off()
