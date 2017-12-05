import colorsys

from blinkstick import blinkstick


def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return r, g, b


class BlinkstickHelper(blinkstick.BlinkStickPro):
    def __init__(self, led_count, serial):
        self.led_count = led_count

        super(BlinkstickHelper, self).__init__(
            r_led_count=led_count,
            g_led_count=led_count,
            b_led_count=led_count,
            delay=0.2)
        self.connect(serial=serial)
        self.buffer = []
        for _ in range(led_count):
            self.push((0, 0, 0))
        self.show()

    def push(self, rgb):
        self.buffer.insert(0, rgb)
        while len(self.buffer) > self.led_count:
            self.buffer.pop()

    def show(self):
        for index in range(self.led_count):
            rgb = self.buffer[index]
            self.set_color(0, index, rgb[0], rgb[1], rgb[2])
        self.send_data_all()

    def push_show(self, rgb):
        self.push(rgb)
        self.show()