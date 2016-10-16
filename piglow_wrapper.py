import datetime
import time
import logging


class PiGlowWrapper(object):
    def __init__(self, pg):
        self._piglow = pg
        self.v = 8
        self._init()
        self.every_hour()
        self.every_minute()

    def _init(self):
        for _ in range(2):
            self._piglow.all(1)
            time.sleep(1)
            self._piglow.all(0)
            time.sleep(1)

    def every_hour(self):
        hour = datetime.datetime.now().hour % 12
        for led in range(18):
            if led <= hour:
                self._piglow.led(led, self.v)
            else:
                self._piglow.led(led, 0)

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
