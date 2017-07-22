import pprint
import random

import time
from phue import Bridge

light_name = "Hue color lamp 1"
bridge_ip = '192.168.0.20'
light = None


def wait():
    time.sleep(1)


def on():
    light.on = True


def colour_temperature(temp):
    # (white only) 154 is the coolest, 500 is the warmest
    light.ct = temp
    wait()


def xy(x, y):
    #  co-ordinates in CIE 1931 space
    light.xy = (x, y)
    wait()


def random_colour():
    light.xy = [random.random(), random.random()]
    wait()


def hue(hue, sat):
    # hue' parameter has the range 0-65535 so represents approximately 182*degrees
    light.hue = hue
    light.sat = sat
    wait()


def colour_loop():
    light.effect = "colorloop"
    wait()


def off():
    light.on = False


if __name__ == '__main__':
    b = Bridge(bridge_ip)
    b.connect()
    for l in b.lights:
        text = l.name
        if l.name == light_name:
            text += " *"
            light = l
        print(text)

    # light.transitiontime = 10  # deciseconds

    on()
    for _ in range(5):
        random_colour()

    colour_temperature(154)
    colour_temperature(500)
    colour_temperature(154)
    colour_loop()
    off()
