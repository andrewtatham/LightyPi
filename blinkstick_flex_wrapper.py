import datetime
import random
from blinkstick import blinkstick
import colorsys
import time


def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return r, g, b


class BlinkstickFlexWrapper(blinkstick.BlinkStickPro):
    def __init__(self, led_count=32):
        self.led_count = led_count
        self.h_start = 0.0
        self.h = 0.0
        self.s = 1.0
        self.v = 0.1
        super(BlinkstickFlexWrapper, self).__init__(
            r_led_count=led_count,
            g_led_count=led_count,
            b_led_count=led_count,
            delay=0.2)
        self.connect(serial="BS006639-3.1")
        self.hello()

    def every_hour(self):

        h = (random.uniform(0.25, 0.75)) % 1.0
        h_alt = (h + random.uniform(0.25, 0.75)) % 1.0

        rgb = hsv_to_rgb(h, self.s, self.v)
        rgb_alt = hsv_to_rgb(h_alt, self.s, self.v)

        for repeat in range(4):
            for alternating in [0, 1]:
                for index in range(self.led_count):

                    if index % 2 == alternating:
                        self.set_color(0, index, rgb[0], rgb[1], rgb[2])
                    else:
                        self.set_color(0, index, rgb_alt[0], rgb_alt[1], rgb_alt[2])
                self.send_data_all()

        self.every_minute()

    def every_minute(self, now=None):
        if not now:
            now = datetime.datetime.now()
        month = now.month
        minute = now.minute
        hour = now.hour
        led = int(minute / 2)
        h = (month / 12.0 + hour / 24.0 + minute / 60.0) % 1.0
        rgb = hsv_to_rgb(h, self.s, self.v)
        self.clear()
        self.set_color(0, 1 + led, rgb[0], rgb[1], rgb[2])
        self.send_data_all()

    def hello(self):
        h_delta = 0.5 / 32
        for led in range(32):
            self.h += h_delta
            rgb = hsv_to_rgb(self.h, self.s, self.v)
            self.set_color(0, led, rgb[0], rgb[1], rgb[2])
        self.send_data_all()

    def rainbow(self):
        h_delta = 0.5 / 32
        while True:
            self.h_start += h_delta
            self.h = self.h_start
            for led in range(32):
                self.h += h_delta
                rgb = hsv_to_rgb(self.h, self.s, self.v)
                self.set_color(0, led, rgb[0], rgb[1], rgb[2])
            self.send_data_all()

    def push(self, hex):
        print("TODO PUSh {}" % hex)


if __name__ == '__main__':
    bs = BlinkstickFlexWrapper()
    try:

        bs.rainbow()

    # bs.every_hour()
    # for minutes in range(60):
    #     now = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
    #     bs.every_minute(now)
    #
    # bs.every_hour()
    except KeyboardInterrupt:
        bs.off()
