import colorsys
import datetime
import logging
import platform
import pprint
import time

import colour
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from blinkstick import blinkstick

import helper.colour_helper
import helper.ping_helper
from cube_stuff import cube_wrapper

try:
    from misc import sportball
except Exception as ex:
    print(ex)

import piglow_wrapper
from aws.aws_wrapper import AwsClient, AwsIotButtonEvent

try:
    from blinksticks.blinkstick_flex_wrapper import BlinkstickFlexWrapper
    from blinksticks.blinkstick_nano_wrapper import BlinkstickNanoWrapper
except Exception as ex:
    print(ex)
from cheerlights.cheerlights_wrapper import CheerlightsWrapper
from hue.phillips_hue_wrapper import HueWrapper
from astral import Astral


class MuteFilter(object):
    def filter(self, record):
        return False


BUTTON_TOPIC = "iotbutton/G030PT020186PK4G"
FOOBAR_TOPIC = "foo/bar"

at_midnight = CronTrigger(hour=0)
on_the_hour = CronTrigger(minute=0)
on_the_minute = CronTrigger(minute="1-59", second=0)
every_second = CronTrigger(second="*")
before_morning = CronTrigger(hour=5, minute=59)
at_morning = CronTrigger(hour=6)
at_bedtime = CronTrigger(hour=23)
every_fifteen_minutes = CronTrigger(minute="*/15")
every_five_minutes = CronTrigger(minute="*/5")
every_minute = CronTrigger(minute="*")

tz = pytz.timezone("Europe/London")


def _get_cron_trigger_for_datetime(dt):
    return CronTrigger(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour, minute=dt.minute, second=dt.second)


class LightyPi(object):
    def __init__(self):
        self.blinksticks = None
        self.blinkstick_nano = None
        self.blinkstick_flex = None
        self.piglow = None
        self.aws = None
        self.cheer = None
        self.hue = None
        self._cube = None
        self.scheduler = BlockingScheduler()
        self.is_linux = platform.platform().startswith('Linux')
        self._initialize()

    def _initialize(self):
        self._init_logging()
        self._init_blinksticks()
        self._init_hue()

        if self.is_linux:
            self._init_piglow()
            # self._init_aws()
            self._init_cheerlights()
            self._init_cube()

    def _init_aws(self):
        self.aws = AwsClient()

    def _init_cheerlights(self):
        self.cheer = CheerlightsWrapper()

    def _init_hue(self):
        self.hue = HueWrapper()
        self.hue.connect()

    def _init_logging(self):
        logging.basicConfig(level=logging.INFO)
        logging.getLogger("apscheduler.scheduler").addFilter(MuteFilter())

    def _init_blinksticks(self):
        blinksticks = blinkstick.find_all()
        self.blinksticks = []
        for bstick in blinksticks:
            description = bstick.get_description()
            logging.info("{} {}".format(bstick.get_serial(), description))
            if description == "BlinkStick Nano":
                self.blinkstick_nano = BlinkstickNanoWrapper()
                self.blinksticks.append(self.blinkstick_nano)
            elif description == "BlinkStick Flex":
                self.blinkstick_flex = BlinkstickFlexWrapper()
                self.blinksticks.append(self.blinkstick_flex)
            else:
                logging.info("UNKNOWN {}".format(description))

    def _init_piglow(self):
        try:
            self.piglow = piglow_wrapper.get()
            if self.piglow:
                logging.info("piglow")
        except Exception as ex:
            logging.warning(ex)

    def _init_cube(self):
        try:
            self._cube = cube_wrapper.get()
            if self._cube:
                logging.info("cube")
        except Exception as ex:
            logging.warning(ex)

    def aws_callback(self, client, userdata, message):
        logging.info("Received a new message: ")
        logging.info(message.payload)
        logging.info("from topic: ")
        logging.info(message.topic)
        logging.info("--------------\n\n")
        if message.topic == BUTTON_TOPIC:
            event = AwsIotButtonEvent(message.payload)
            if event.is_single:
                if self.blinkstick_flex:
                    self.blinkstick_flex.hello()

    def cheerlights_callback(self, hex):
        logging.info("cheerlights {}".format(hex))
        r, g, b = colour.web2rgb(hex)
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        if self.hue:
            self.hue.set_hsv(h, s, v)

        v = 0.05
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        rgb = (r, g, b)
        logging.info("cheerlights {}".format(rgb))
        if self.blinkstick_flex:
            self.blinkstick_flex.push_show(rgb)
        if self.blinkstick_nano:
            self.blinkstick_nano.push_show(rgb)

    def shutdown(self):
        logging.info("shutdown")
        if self.scheduler:
            self.scheduler.shutdown()
        if self.aws:
            self.aws.shutdown()
        self.lights_off()

    def lights_on(self):
        for blinkstick in self.blinksticks:
            blinkstick.enable()
        if self.piglow:
            self.piglow.on()
        if self.hue:
            self.hue.on()
        if self._cube:
            self._cube.on()

    def lights_off(self):
        for blinkstick in self.blinksticks:
            blinkstick.disable()
        if self.piglow:
            self.piglow.off()
        if self.hue:
            self.hue.off()
        if self._cube:
            self._cube.off()

    def run(self):
        self.scheduler.print_jobs()
        self.scheduler.start()

    def piglow_clock(self):
        if self.piglow:
            self.scheduler.add_job(func=self.piglow.update_time, trigger=every_second)

    def cheerlights_subscribe(self):
        if self.cheer:
            self.scheduler.add_job(func=self.cheer.check, trigger=on_the_minute)
            self.cheer.subscribe(self.cheerlights_callback)

    def cheerlights_history(self):
        if self.cheer:
            hex_list = self.cheer.history()
            for hex in hex_list:
                self.cheerlights_callback(hex)

    def aws_iot_button_subscribe(self):
        if self.aws:
            self.aws.subscribe(BUTTON_TOPIC, self.aws_callback)

    def aws_foobar_subscribe(self):
        if self.aws:
            self.aws.subscribe(FOOBAR_TOPIC, self.aws_callback)

    def _aws_foobar_publish(self):
        if self.aws:
            self.aws.publish(FOOBAR_TOPIC, datetime.datetime.now().strftime("%X"))

    def aws_foobar_publish(self):
        if self.aws:
            self.scheduler.add_job(self._aws_foobar_publish, on_the_minute)

    def _xmas(self):
        if self.piglow:
            self.piglow.xmas()
        for blinkstick in self.blinksticks:
            blinkstick.xmas()

    def xmas(self):
        self.scheduler.add_job(func=self._xmas, trigger=every_second)

    def at_midnight_get_sun_data(self):
        self.scheduler.add_job(func=self._get_sunset_sunrise, trigger=at_midnight)
        self.scheduler.add_job(func=self._get_sunset_sunrise)

    def _get_sunset_sunrise(self):
        a = Astral()
        leeds = a['Leeds']
        today = datetime.date.today()
        self._today_sun_data = leeds.sun(date=today, local=True)
        self.timezone = leeds.timezone
        logging.info(pprint.pformat(self._today_sun_data))

        self.dawn = self._today_sun_data['dawn']
        self.sunrise = self._today_sun_data['sunrise']
        self.sunset = self._today_sun_data['sunset']
        self.dusk = self._today_sun_data['dusk']

        at_dawn = _get_cron_trigger_for_datetime(self.dawn)
        at_sunrise = _get_cron_trigger_for_datetime(self.sunrise)
        at_sunset = _get_cron_trigger_for_datetime(self.sunset)
        at_dusk = _get_cron_trigger_for_datetime(self.dusk)

        during_sunrise = IntervalTrigger(seconds=5, start_date=self.dawn, end_date=self.sunrise)
        during_sunset = IntervalTrigger(seconds=5, start_date=self.sunset, end_date=self.dusk)

        self.scheduler.add_job(func=self._at_dawn, trigger=at_dawn)
        self.scheduler.add_job(func=self._during_sunrise, trigger=during_sunrise)
        self.scheduler.add_job(func=self._at_sunrise, trigger=at_sunrise)

        self.scheduler.add_job(func=self._at_sunset, trigger=at_sunset)
        self.scheduler.add_job(func=self._during_sunset, trigger=during_sunset)
        self.scheduler.add_job(func=self._at_dusk, trigger=at_dusk)

        now = datetime.datetime.now(tz)
        if now <= self.dawn:
            day_factor = 0.0
        elif self.dawn < now <= self.sunrise:
            day_factor = helper.colour_helper.get_day_factor(self.dawn, now, self.sunrise, True)
        elif self.sunrise < now <= self.sunset:
            day_factor = 1.0
        elif self.sunset < now <= self.dusk:
            day_factor = helper.colour_helper.get_day_factor(self.sunset, now, self.dusk, False)
        elif now < self.dusk:
            day_factor = 0.0
        else:
            day_factor = 0.25

        self._set_day_factor(day_factor)

    def _at_dawn(self):
        day_factor = 0.0
        self._set_day_factor(day_factor)
        logging.info('dawn')

    def _at_sunrise(self):
        day_factor = 1.0
        self._set_day_factor(day_factor)
        logging.info('sunrise')

    def _at_sunset(self):
        day_factor = 1.0
        self._set_day_factor(day_factor)
        logging.info('sunset')

    def _at_dusk(self):
        day_factor = 0.0
        self._set_day_factor(day_factor)
        logging.info('dusk')

    def _during_sunrise(self):
        day_factor = helper.colour_helper.get_day_factor(self.dawn, datetime.datetime.now(tz), self.sunrise, True)
        self._set_day_factor(day_factor)

    def _during_sunset(self):
        day_factor = helper.colour_helper.get_day_factor(self.sunset, datetime.datetime.now(tz), self.dusk, False)
        self._set_day_factor(day_factor)

    def _set_day_factor(self, day_factor):
        logging.info('day factor: {}'.format(day_factor))
        helper.colour_helper.set_day_factor(day_factor)

    def larsson_scanner(self):
        self.scheduler.add_job(self._larsson_scanner, at_morning)
        self.scheduler.add_job(self._larsson_scanner)  # omit trigger = run at startup

    def _larsson_scanner(self):
        if self.blinkstick_flex:
            self._wait_for_brightness()
            self.blinkstick_flex.larsson_scanner()

    def sportball(self):
        self.scheduler.add_job(self._sportball, every_fifteen_minutes)

    def _sportball(self):
        sportball.update()

    def cube_job(self):
        self.scheduler.add_job(self._cube_job, at_morning)
        self.scheduler.add_job(self._cube_job)  # omit trigger = run at startup

    def _cube_job(self):
        if self._cube:
            self._wait_for_brightness()
            self._cube.run()

    def _wait_for_brightness(self):
        while helper.colour_helper.brightness is None:
            print("waiting for brightness value")
            time.sleep(1)

    def ping_andrewdesktop(self):
        self.scheduler.add_job(func=self._ping_andrewdesktop, trigger=every_fifteen_minutes)
        self.scheduler.add_job(func=self._ping_andrewdesktop)

    def _ping_andrewdesktop(self):
        andrewdesktop_is_up = helper.ping_helper.ping_andrewdesktop()
        if andrewdesktop_is_up and not helper.colour_helper.is_on:
            print("andrewdesktop switched on")
            self.lights_on()
        elif not andrewdesktop_is_up and helper.colour_helper.is_on:
            print("andrewdesktop switched off")
            self.lights_off()
        helper.colour_helper.is_on = andrewdesktop_is_up

    def hue_colour_loop(self):
        self.scheduler.add_job(func=self._hue_next_profile, trigger=every_fifteen_minutes)
        self.scheduler.add_job(func=self._hue_do_whatever, trigger=every_minute)
        self.scheduler.add_job(func=self._hue_do_whatever)

    def _hue_do_whatever(self):
        if self.hue:
            self._wait_for_brightness()
            self.hue.do_whatever()

    def _hue_next_profile(self):
        if self.hue:
            self.hue.next_profile()


if __name__ == '__main__':
    pi = LightyPi()
    # pi.ping_andrewdesktop()
    pi.at_midnight_get_sun_data()
    pi.larsson_scanner()
    pi.hue_colour_loop()
    try:
        pi.run()
    except KeyboardInterrupt:
        pass
    finally:
        pi.shutdown()
