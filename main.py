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

BUTTON_TOPIC = "iotbutton/G030PT020186PK4G"


class MuteFilter(object):
    def filter(self, record):
        return False


blinkstick_nano = None
blinkstick_flex = None
piglow = None
aws = None
cheer = None
hue = None

_platform = platform.platform()
is_linux = _platform.startswith('Linux')


def _initialize():
    global aws, cheer, hue
    _init_logging()
    _init_blinksticks()
    if is_linux:
        _init_piglow()
        aws = AwsClient()
    cheer = CheerlightsWrapper()
    hue = HueWrapper()
    hue.connect()


def _init_logging():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("apscheduler.scheduler").addFilter(MuteFilter())


def _init_blinksticks():
    global blinkstick_nano, blinkstick_flex
    blinksticks = blinkstick.find_all()
    for bstick in blinksticks:
        description = bstick.get_description()
        print(bstick.get_serial(), description)
        if description == "BlinkStick Nano":
            blinkstick_nano = BlinkstickNanoWrapper()
        elif description == "BlinkStick Flex":
            blinkstick_flex = BlinkstickFlexWrapper()
        else:
            print("UNKNOWN {}".format(description))


def _init_piglow():
    global piglow
    try:
        piglow = piglow_wrapper.get()
        print("piglow")
    except Exception as ex:
        logging.warning(ex)


def _shutdown():
    if blinkstick_nano:
        blinkstick_nano.off()
    if blinkstick_flex:
        blinkstick_flex.off()
    if piglow:
        piglow.off()
    hue.off()


def aws_callback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    if message.topic == BUTTON_TOPIC:
        event = AwsIotButtonEvent(message.payload)
        if event.is_single:
            if blinkstick_flex:
                blinkstick_flex.hello()


def cheerlights_callback(hex):
    print("cheerlights {}".format(hex))
    r, g, b = colour.web2rgb(hex)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    hue.set_hsv(h, s, v)
    v = 0.05
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    rgb = (r, g, b)
    print("cheerlights {}".format(rgb))
    if blinkstick_flex:
        blinkstick_flex.push_show(rgb)
    if blinkstick_nano:
        blinkstick_nano.push_show(rgb)


def publish():
    aws.publish("foo/bar", datetime.datetime.now().strftime("%X"))


if __name__ == '__main__':
    try:

        _initialize()
        scheduler = BlockingScheduler()

        on_the_hour = CronTrigger(minute=0)
        on_the_minute = CronTrigger(minute="1-59", second=0)
        every_second = CronTrigger(second="*")

        if piglow:
            scheduler.add_job(func=piglow.every_second, trigger=every_second)

        if aws:
            aws.subscribe(BUTTON_TOPIC, aws_callback)
            # aws.subscribe("foo/bar", aws_callback)
            # scheduler.add_job(publish, on_the_minute)
        if cheer:
            scheduler.add_job(func=cheer.check, trigger=on_the_minute)
            cheer.subscribe(cheerlights_callback)
            hex_list = cheer.history()

            for hex in hex_list:
                cheerlights_callback(hex)

        scheduler.print_jobs()
        scheduler.start()

    except KeyboardInterrupt:
        scheduler.shutdown()
    finally:
        _shutdown()
