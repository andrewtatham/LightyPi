import datetime
import logging
import platform

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from blinkstick import blinkstick

import train_check
import piglow_wrapper
from aws_wrapper import AwsClient, AwsIotButtonEvent
from blinkstick_flex_wrapper import BlinkstickFlexWrapper
from blinkstick_nano_wrapper import BlinkstickNanoWrapper
from cheerlights_wrapper import CheerlightsWrapper

BUTTON_TOPIC = "iotbutton/G030PT020186PK4G"


class MuteFilter(object):
    def filter(self, record):
        return False


blinkstick_nano = None
blinkstick_flex = None
piglow = None
aws = None
cheer = None

_platform = platform.platform()
is_linux = _platform.startswith('Linux')


def _initialize():
    global aws, cheer
    _init_logging()
    _init_blinksticks()
    if is_linux:
        _init_piglow()
        aws = AwsClient()
    cheer = CheerlightsWrapper()


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


def is_my_fucking_train_on_time():
    response = train_check.is_my_fucking_train_on_time()
    if piglow:
        piglow.is_my_train_on_time(response)


def trains_off():
    if piglow:
        piglow.trains_off()


# Custom MQTT message callback
def customCallback(client, userdata, message):
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


def check_cheerlights():
    cheer.check()


def cheerlights_callback(hex):
    print("cheerlights {}" % hex)
    if blinkstick_flex:
        blinkstick_flex.push(hex)


def publish():
    aws.publish("foo/bar", datetime.datetime.now().strftime("%X"))


if __name__ == '__main__':

    trackCommute = False
    _initialize()
    scheduler = BlockingScheduler()

    on_the_hour = CronTrigger(minute=0)
    on_the_minute = CronTrigger(minute="1-59", second=0)
    every_second = CronTrigger(second="*")

    morning_commute_6 = CronTrigger(hour=6, minute="20-59/5", day_of_week="MON-FRI")
    morning_commute_7 = CronTrigger(hour=7, minute="0-40/5", day_of_week="MON-FRI")
    evening_commute = CronTrigger(hour=16, minute="0-38/5", day_of_week="MON-FRI")
    morning_commute_off = CronTrigger(hour=7, minute=42, day_of_week="MON-FRI")
    evening_commute_off = CronTrigger(hour=16, minute=40, day_of_week="MON-FRI")

    if piglow:
        scheduler.add_job(func=piglow.every_second, trigger=every_second)
    if blinkstick_flex:
        scheduler.add_job(func=blinkstick_flex.every_hour, trigger=on_the_hour)
        scheduler.add_job(func=blinkstick_flex.every_minute, trigger=on_the_minute)
    if blinkstick_nano:
        scheduler.add_job(func=blinkstick_nano.every_hour, trigger=on_the_hour)
        scheduler.add_job(func=blinkstick_nano.every_minute, trigger=on_the_minute)
    if piglow and trackCommute:
        scheduler.add_job(func=is_my_fucking_train_on_time, trigger=morning_commute_6)
        scheduler.add_job(func=is_my_fucking_train_on_time, trigger=morning_commute_7)
        scheduler.add_job(func=is_my_fucking_train_on_time, trigger=evening_commute)
        scheduler.add_job(func=trains_off, trigger=morning_commute_off)
        scheduler.add_job(func=trains_off, trigger=evening_commute_off)



    try:
        if aws:
            aws.subscribe(BUTTON_TOPIC, customCallback)
            aws.subscribe("foo/bar", customCallback)
            scheduler.add_job(publish, on_the_minute)
        if cheer:
            scheduler.add_job(func=check_cheerlights, trigger=on_the_minute)
            cheer.subscribe(cheerlights_callback)
            if blinkstick_flex:
                hex_list = cheer.history()
                for hex in hex_list:
                    blinkstick_flex.push(hex)

        scheduler.print_jobs()
        scheduler.start()

    except KeyboardInterrupt:
        scheduler.shutdown()
    finally:
        _shutdown()
