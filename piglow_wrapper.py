import datetime
import time
import logging

hour_mapping = {

    1: 10,
    2: 9,
    3: 8,
    4: 7,

    5: 16,
    6: 15,
    7: 14,
    8: 13,

    9: 4,
    10: 3,
    11: 2,
    12: 1
}


class PiGlowWrapper(object):
    def __init__(self, pg):
        self._piglow = pg
        self.on = 2
        self._init()
        self.every_hour()
        self.every_minute()

    def _init(self):
        for _ in range(2):
            self._piglow.all(self.on)
            time.sleep(1)
            self._piglow.all(0)
            time.sleep(1)

    def every_hour(self):

        hour = datetime.datetime.now().hour % 12
        if hour == 0:
            hour = 12
        on_led = hour_mapping[hour]
        for led in range(18):
            piglow_led = led + 1
            if piglow_led == on_led:
                self._piglow.led(piglow_led, self.on)
            else:
                self._piglow.led(piglow_led, 0)

    def every_minute(self):
        pass

    def off(self):
        self._piglow.all(0)


def get():
    try:
        import sys
        sys.path.append("piglow")
        import piglow
        return PiGlowWrapper(piglow.PiGlow())
    except Exception as ex:
        logging.warning(ex)


if __name__ == '__main__':
    pg = get()
    pg.every_hour()
    for _ in range(60):
        pg.every_minute()
