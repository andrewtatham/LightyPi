import datetime
import random

from blinkstick import blinkstick

from blinkstick_flex_wrapper import hsv_to_rgb


class BlinkstickNanoWrapper(blinkstick.BlinkStickPro):
    def __init__(self, led_count=2):
        self.led_count = led_count

        self.h = 0.0
        self.s = 1.0
        self.v = 0.1

        self.h_alt = None
        super(BlinkstickNanoWrapper, self).__init__(
            r_led_count=led_count,
            g_led_count=led_count,
            b_led_count=led_count,

            delay=0.2)
        self.connect(serial="BS003518-3.0")
        self.every_hour()
        self.every_minute()

    def every_minute(self):
        self.off()
        self.h = (self.h + random.uniform(0.25, 0.75)) % 1.0
        self.h_alt = (self.h + random.uniform(0.25, 0.75)) % 1.0

        rgb = hsv_to_rgb(self.h, self.s, self.v)
        rgb_alt = hsv_to_rgb(self.h_alt, self.s, self.v)
        for repeat in range(4):
            for alternating in [0, 1]:
                for index in range(self.led_count):
                    if index % 2 == alternating:
                        self.set_color(0, index, rgb[0], rgb[1], rgb[2])
                    else:
                        self.set_color(0, index, rgb_alt[0], rgb_alt[1], rgb_alt[2])
                self.send_data_all()
        self.off()

    def every_hour(self):
        self.off()
        hour = datetime.datetime.now().hour % 12
        for _ in range(hour):
            for led in range(self.led_count):
                self.set_color(channel=0, index=led, r=8, g=8, b=8)
            self.send_data_all()
            for led in range(self.led_count):
                self.set_color(channel=0, index=led, r=0, g=0, b=0)
            self.send_data_all()

        self.off()


if __name__ == '__main__':
    bs = BlinkstickNanoWrapper()
    bs.every_hour()
    for _ in range(60):
        bs.every_minute()
    bs.every_hour()
    bs.off()
