import datetime
import time
import logging
import platform
import colorsys
import colour

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from blinkstick import blinkstick

import train_check
import piglow_wrapper
from aws_wrapper import AwsClient, AwsIotButtonEvent
from blinkstick_flex_wrapper import BlinkstickFlexWrapper
from blinkstick_nano_wrapper import BlinkstickNanoWrapper
from cheerlights_wrapper import CheerlightsWrapper
from phillips_hue_wrapper import HueWrapper


class MuteFilter(object):
    def filter(self, record):
        return False


BUTTON_TOPIC = "iotbutton/G030PT020186PK4G"
FOOBAR_TOPIC = "foo/bar"

on_the_hour = CronTrigger(minute=0)
on_the_minute = CronTrigger(minute="1-59", second=0)
every_second = CronTrigger(second="*")


class LightyPi():
    def __init__(self):
        self.blinksticks = None
        self.blinkstick_nano = None
        self.blinkstick_flex = None
        self.piglow = None
        self.aws = None
        self.cheer = None
        self.hue = None
        self.scheduler = BlockingScheduler()
        self.is_linux = platform.platform().startswith('Linux')
        self._initialize()

    def _initialize(self):
        self._init_logging()
        self._init_blinksticks()
        if self.is_linux:
            self._init_piglow()
            # self._init_aws()
            # self._init_cheerlights()
            # self._init_hue()

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
            print(bstick.get_serial(), description)
            if description == "BlinkStick Nano":
                self.blinkstick_nano = BlinkstickNanoWrapper()
                self.blinksticks.append(self.blinkstick_nano)
            elif description == "BlinkStick Flex":
                self.blinkstick_flex = BlinkstickFlexWrapper()
                self.blinksticks.append(self.blinkstick_flex)
            else:
                print("UNKNOWN {}".format(description))

    def _init_piglow(self):
        try:
            self.piglow = piglow_wrapper.get()
            print("piglow")
        except Exception as ex:
            logging.warning(ex)

    def aws_callback(self, client, userdata, message):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")
        if message.topic == BUTTON_TOPIC:
            event = AwsIotButtonEvent(message.payload)
            if event.is_single:
                if self.blinkstick_flex:
                    self.blinkstick_flex.hello()

    def cheerlights_callback(self, hex):
        print("cheerlights {}".format(hex))
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
        print("cheerlights {}".format(rgb))
        if self.blinkstick_flex:
            self.blinkstick_flex.push_show(rgb)
        if self.blinkstick_nano:
            self.blinkstick_nano.push_show(rgb)

    def shutdown(self):
        print("shutdown")
        if self.scheduler:
            self.scheduler.shutdown()
        if self.aws:
            self.aws.shutdown()
        for blinkstick in self.blinksticks:
            blinkstick.off()
        if self.piglow:
            self.piglow.off()
        if self.hue:
            self.hue.off()

    def run(self):
        self.scheduler.print_jobs()
        self.scheduler.start()

    def piglow_clock(self):
        if self.piglow:
            self.scheduler.add_job(func=self.piglow.every_second, trigger=every_second)

    def cheerlights_subscribe(self):
        if self.cheer:
            self.scheduler.add_job(func=self.cheer.check, trigger=on_the_minute)
            self.cheer.subscribe(cheerlights_callback)

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


if __name__ == '__main__':
    pi = LightyPi()

    try:
        pi.run()
    except KeyboardInterrupt:
        pass
    finally:
        pi.shutdown()
