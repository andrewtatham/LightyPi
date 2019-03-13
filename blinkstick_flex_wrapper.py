import time

import colour_helper
from blinkstick_helper import BlinkstickHelper


def h_delta(h, delta):
    h += delta
    h %= 1.0
    return h


class LarssonScanner(object):
    def __init__(self, blinkstick_flex):
        self.blinkstick_flex = blinkstick_flex
        self.led_count = len(self.blinkstick_flex.buffer)
        self._index = 0
        self._direction = True

    def run(self):
        h = 0
        while self.blinkstick_flex.is_enabled:
            h = h_delta(h, 0.001)
            hsv = (h, 1.0, colour_helper.v)
            self._run(hsv)
            time.sleep(0.1)
        still_on = True
        while still_on:
            time.sleep(1)
            still_on = self.blinkstick_flex.fade()
            self.blinkstick_flex.show()

    def _run(self, hsv):
        if self.blinkstick_flex.is_enabled:
            self.blinkstick_flex.fade()
            if self._direction:
                self._index += 1
            else:
                self._index -= 1
            if self._index <= 0:
                self._direction = True
                self._index = 0
            if self._index >= self.led_count - 1:
                self._direction = False
                self._index = self.led_count - 1

            self.blinkstick_flex.buffer[self._index] = hsv
            self.blinkstick_flex.show()


class BlinkstickFlexWrapper(BlinkstickHelper):
    def __init__(self, led_count=32, serial="BS006639-3.1"):
        BlinkstickHelper.__init__(self, led_count, serial)
        self._larsson_scanner = LarssonScanner(self)

    def larsson_scanner(self):
        self._larsson_scanner.run()


if __name__ == '__main__':
    bs = BlinkstickFlexWrapper()
    try:
        bs.larsson_scanner()
    except KeyboardInterrupt:
        pass
    finally:
        bs.off()
