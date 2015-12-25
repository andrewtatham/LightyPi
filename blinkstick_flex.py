import random

from blinkstick import blinkstick

import colorsys


def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return r, g, b


class BlinkstickFlexWrapper(blinkstick.BlinkStickPro):
    def __init__(self, led_count=32):
        self.led_count = led_count
        self.h = 0.0
        self.s = 1.0
        self.v = 1.0

        super(BlinkstickFlexWrapper, self).__init__(
            r_led_count=led_count,
            g_led_count=led_count,
            b_led_count=led_count,

            delay=0.05)
        self.connect(serial="BS006639-3.1")

    def rainbow(self):

        self.off()
        self.h = (self.h + random.uniform(0.25, 0.75)) % 1.0
        h_alt = (self.h + random.uniform(0.25, 0.75)) % 1.0

        rgb = hsv_to_rgb(self.h, self.s, self.v)
        rgb_alt = hsv_to_rgb(h_alt, self.s, self.v)
        for repeat in range(4):
            for alternating in [0, 1]:
                for index in range(self.led_count):

                    if index % 2 == alternating:
                        self.set_color(0, index, rgb[0], rgb[1], rgb[2])
                    else:
                        self.set_color(0, index, rgb_alt[0], rgb_alt[1], rgb_alt[2])
                self.send_data_all()
        self.off()


if __name__ == '__main__':
    main = BlinkstickFlexWrapper()
    main.rainbow()
