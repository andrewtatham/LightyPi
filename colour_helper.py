import colorsys
import random

rgb_black = (0, 0, 0)


def get_random_hsv():
    h = random.uniform(0.0, 1.0)
    s = 1.0
    v = brightness
    return h, s, v


def get_random_rgb():
    return hsv_to_rgb(get_random_hsv())


def h_delta(hsv, h_delta):
    h, s, v = hsv
    h = (h + h_delta) % 1.0
    return h, s, v


def hsv_to_rgb(hsv):
    h = hsv[0]
    s = hsv[1]
    v = hsv[2]
    rgb = colorsys.hsv_to_rgb(h, s, v)
    r = int(rgb[0])
    g = int(rgb[1])
    b = int(rgb[2])
    return r, g, b


def set_day_factor(_day_factor):
    global day_factor, brightness
    day_factor = _day_factor
    brightness = int(8 + 64 * day_factor)


day_factor = None
brightness = None
set_day_factor(1.0)
