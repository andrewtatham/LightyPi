import logging
import platform

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from blinkstick import blinkstick

import piglow_wrapper
from blinkstick_flex_wrapper import BlinkstickFlexWrapper
from blinkstick_nano_wrapper import BlinkstickNanoWrapper

blinkstick_nano = None
blinkstick_flex = None
piglow = None

_platform = platform.platform()
is_linux = _platform.startswith('Linux')


def _initialize():
    _init_blinksticks()
    if is_linux:
        _init_piglow()


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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    _initialize()
    scheduler = BlockingScheduler()

    on_the_hour = CronTrigger(minute=0)
    on_the_minute = CronTrigger(minute="1-59", second=0)

    if piglow:
        scheduler.add_job(func=piglow.every_hour, trigger=on_the_hour)
        scheduler.add_job(func=piglow.every_minute, trigger=on_the_minute)
    if blinkstick_flex:
        scheduler.add_job(func=blinkstick_flex.every_hour, trigger=on_the_hour)
        scheduler.add_job(func=blinkstick_flex.every_minute, trigger=on_the_minute)
    if blinkstick_nano:
        scheduler.add_job(func=blinkstick_nano.every_hour, trigger=on_the_hour)
        scheduler.add_job(func=blinkstick_nano.every_minute, trigger=on_the_minute)
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()
    finally:
        _shutdown()
