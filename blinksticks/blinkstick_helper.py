import colorsys
import pprint

import itertools
from blinkstick import blinkstick


def _limit(minimum, value, maximum):
    return max(minimum, min(value, maximum))


def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r = _limit(0, int(r), 255)
    g = _limit(0, int(g), 255)
    b = _limit(0, int(b), 255)
    return r, g, b


def hsv_to_rgb2(hsv):
    r, g, b = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
    r = _limit(0, int(r), 255)
    g = _limit(0, int(g), 255)
    b = _limit(0, int(b), 255)
    return r, g, b


s = 1.0
v = 0.05


def rgb_to_hsv(rgb):
    hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    return hsv


def fade_hsv(hsv):
    fade_delta = max(1, int(hsv[2] / 8))
    v_new = _limit(0, int(hsv[2] - fade_delta), 255)
    return hsv[0], hsv[1], v_new


black = rgb_to_hsv((0, 0, 0))


class BlinkstickHelper(blinkstick.BlinkStickPro):
    def __init__(self, led_count, serial):
        self.led_count = led_count

        super(BlinkstickHelper, self).__init__(
            r_led_count=led_count,
            g_led_count=led_count,
            b_led_count=led_count)
        self.connect(serial=serial)
        self.is_enabled = True
        self.buffer = []
        for _ in range(led_count):
            self.push(black)
        self.show()

        red = 1.0
        green = 1.0 / 3.0
        self.xmas_hs = itertools.cycle([red, green])

    def push(self, hsv):
        if self.is_enabled:
            self.buffer.insert(0, hsv)
            while len(self.buffer) > self.led_count:
                self.buffer.pop()

    def show(self):
        for index in range(self.led_count):
            hsv = self.buffer[index]
            rgb = hsv_to_rgb2(hsv)
            self.set_color(0, index, rgb[0], rgb[1], rgb[2])
        self.send_data_all()

    def fade(self):
        still_on = False
        for index in range(self.led_count):
            hsv = self.buffer[index]
            hsv = fade_hsv(hsv)
            still_on = still_on or hsv[2] > 0
            self.buffer[index] = hsv
        return still_on

    def enable(self):
        self.is_enabled = True
        self.hello()

    def disable(self):
        self.off()
        self.is_enabled = False

    def push_show(self, hsv):
        if self.is_enabled:
            self.push(hsv)
            self.show()

    def hello(self):
        if self.is_enabled:
            h_delta = 1.0 / self.led_count
            h = 0.0
            for t in range(self.led_count):
                for led in range(self.led_count):
                    self.push((h, s, v))
                    h += h_delta
                self.show()
                h += h_delta

    def xmas(self):
        if self.is_enabled:
            h = next(self.xmas_hs)
            self.push_show((h, s, v))

    def all(self, rgb):
        hsv = rgb_to_hsv(rgb)
        for index in range(self.led_count):
            self.buffer[index] = hsv
            self.set_color(0, index, rgb[0], rgb[1], rgb[2])
        self.send_data_all()


if __name__ == '__main__':
    bs = blinkstick.find_all()
    pprint.pprint(bs)
