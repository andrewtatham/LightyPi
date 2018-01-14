import time
from blinkstick_helper import BlinkstickHelper


def h_delta(h, delta):
    h += delta
    h %= 1.0
    return h


class BlinkstickFlexWrapper(BlinkstickHelper):
    def __init__(self, led_count=32, serial="BS006639-3.1"):
        BlinkstickHelper.__init__(self, led_count, serial)
        self.larsson_scanner_index = 0
        self.larsson_scanner_direction = True

    def larsson_scanner(self):
        h = 0
        while self.is_enabled:
            h = h_delta(h, 0.001)
            hsv = (h, 1.0, 64)
            self._larsson_scanner(hsv)
            time.sleep(0.1)
        still_on = True
        while still_on:
            time.sleep(1)
            still_on = self.fade()
            self.show()

    def _larsson_scanner(self, hsv):
        if self.is_enabled:
            self.fade()
            if self.larsson_scanner_direction:
                self.larsson_scanner_index += 1
            else:
                self.larsson_scanner_index -= 1
            if self.larsson_scanner_index <= 0:
                self.larsson_scanner_direction = True
                self.larsson_scanner_index = 0
            if self.larsson_scanner_index >= self.led_count - 1:
                self.larsson_scanner_direction = False
                self.larsson_scanner_index = self.led_count - 1

            self.buffer[self.larsson_scanner_index] = hsv
            self.show()


if __name__ == '__main__':
    bs = BlinkstickFlexWrapper()
    try:
        bs.larsson_scanner()
    except KeyboardInterrupt:
        pass
    finally:
        bs.off()
