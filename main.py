import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from blinkstick import blinkstick

from blinkstick_flex import BlinkstickFlexWrapper
from blinkstick_nano import BlinkstickNanoWrapper

blinkstick_nano = None
blinkstick_flex = None


def _initialize():
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


def _shutdown():
    if blinkstick_nano:
        blinkstick_nano.off()
    if blinkstick_flex:
        blinkstick_flex.off()


if __name__ == '__main__':
    logging.basicConfig()
    _initialize()
    scheduler = BlockingScheduler()

    on_the_hour = CronTrigger(minute=0)

    if blinkstick_flex:
        scheduler.add_job(func=blinkstick_flex.rainbow, trigger=on_the_hour)
    if blinkstick_nano:
        # scheduler.add_job(func=blinkstick_nano.rainbow, trigger=IntervalTrigger(seconds=15))
        scheduler.add_job(func=blinkstick_nano.hourly_chime, trigger=on_the_hour)

    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()
    finally:
        _shutdown()
