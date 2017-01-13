import datetime
import time
import logging

led_mapping = {

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
    def __init__(self, piglow):
        self._piglow = piglow
        self._on = 2
        self._off = 0
        self.prev_hour_led = None
        self.prev_minute_led = None
        self.previous_state = None

        self._init()
        self.update_time()

    def _init(self):
        for _ in range(2):
            self._piglow.all(self._on)
            time.sleep(1)
            self._piglow.all(0)
            time.sleep(1)

    def update_time(self, now=None):
        if not now:
            now = datetime.datetime.now()

        hour = now.hour % 12
        if hour == 0:
            hour = 12
        minute = int(now.minute / 5) + 1

        hour_led = led_mapping[hour]
        minute_led = led_mapping[minute]

        if self.prev_hour_led and self.prev_hour_led != hour_led:
            self._piglow.led(self.prev_hour_led, self._off)
        if self.prev_minute_led and self.prev_minute_led != minute_led:
            self._piglow.led(self.prev_minute_led, self._off)

        self._piglow.led(hour_led, self._on)
        self._piglow.led(minute_led, self._on)

        self.prev_hour_led = hour_led
        self.prev_minute_led = minute_led

    def every_hour(self):
        self.update_time()

    def every_minute(self):
        self.update_time()

    def off(self):
        self._piglow.all(0)

    def is_my_train_on_time(self, train_result):
        state = train_result.TrainState
        if self.previous_state and state != self.previous_state:
            self._set_train_state_lights(self.previous_state, self._off)
        if not self.previous_state or state != self.previous_state:
            self._set_train_state_lights(state, self._on)
        self.previous_state = state
        self.update_time()

    def trains_off(self):
        if self.previous_state:
            self._set_train_state_lights(self.previous_state, self._off)
        self.previous_state = None
        self.update_time()

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
