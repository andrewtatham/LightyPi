import datetime
import time
import logging

led_mapping = {

    0: 10,
    1: 9,
    2: 8,
    3: 7,

    4: 16,
    5: 15,
    6: 14,
    7: 13,

    8: 4,
    9: 3,
    10: 2,
    11: 1
}


class PiGlowWrapper(object):
    def __init__(self, piglow):
        self._piglow = piglow

        self._alt = False
        self._on = 2
        self._alt_on = 3
        self._off = 0

        self._xmas_alt = False

        self.prev_hour_led = None
        self.prev_minute_led = None
        self.previous_state = None

        self._init()
        self.update_time()

    def _init(self):
        for _ in range(2):
            self._piglow.all(self._on)
            time.sleep(1)
            self._piglow.all(self._off)
            time.sleep(1)

    def _update_time(self, now=None):
        if not now:
            now = datetime.datetime.now()

        hour = (now.hour + 11) % 12
        minute = int(((now.minute + 55) % 60) / 5)

        hour_led = led_mapping[hour]
        minute_led = led_mapping[minute]

        if self.prev_hour_led and self.prev_hour_led != hour_led:
            self._piglow.led(self.prev_hour_led, self._off)
        if self.prev_minute_led and self.prev_minute_led != minute_led:
            self._piglow.led(self.prev_minute_led, self._off)

        self._piglow.led(hour_led, self._on)

        if self._alt:
            flashy = self._alt_on
        else:
            flashy = self._on

        self._piglow.led(minute_led, flashy)

        self.prev_hour_led = hour_led
        self.prev_minute_led = minute_led

    def update_time(self):
        self._alt = not self._alt
        self._update_time()

    def off(self):
        self._piglow.all(0)

    def is_my_train_on_time(self, train_result):
        state = train_result.TrainState
        if self.previous_state and state != self.previous_state:
            self._set_train_state_lights(self.previous_state, self._off)
        if not self.previous_state or state != self.previous_state:
            self._set_train_state_lights(state, self._on)
        self.previous_state = state
        self._update_time()

    def trains_off(self):
        if self.previous_state:
            self._set_train_state_lights(self.previous_state, self._off)
        self.previous_state = None
        self._update_time()

    def _set_train_state_lights(self, state, value):
        if state == "Unknown":
            self._piglow.blue(value)
        elif state == "OnTime":
            self._piglow.green(value)
        elif state == "Delayed":
            self._piglow.yellow(value)
        elif state == "Cancelled":
            self._piglow.red(value)
        elif state == "TooFarAhead":
            self._piglow.blue(value)
        elif state == "ServiceDown":
            self._piglow.blue(value)
        elif state == "NoTrains":
            self._piglow.red(value)

    def xmas(self):
        self._xmas_alt = not self._xmas_alt
        if self._xmas_alt:
            self._piglow.Green(self._alt_on)
            self._piglow.Red(self._on)
        else:
            self._piglow.Green(self._on)
            self._piglow.Red(self._alt_on)
        self._update_time()

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
