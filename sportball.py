import ssl
import datetime
import pprint
import time
import re
from colorsys import rgb_to_hsv

from blinkstick import blinkstick
import feedparser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from blinkstick_flex_wrapper import BlinkstickFlexWrapper
from blinkstick_nano_wrapper import BlinkstickNanoWrapper
from phillips_hue_wrapper import HueWrapper
from scrollhat_wrapper import ScrollHatWrapper

feed_url = "https://www.scorespro.com/rss2/live-soccer.xml"
rx = re.compile("^\((\w*)-(\w*)\) (.*) vs (.*): (\d*)-(\d*) - ?(.*)$", re.MULTILINE)


class SportballEvent(object):
    def __init__(self, entry):
        self.entry_summary = entry['summary']
        self.entry_published = entry["published"]
        # print(self.entry_summary)
        match = rx.match(self.entry_summary)
        if match:
            self.country = match.group(1)
            self.league = match.group(2)
            self.home_team = match.group(3)
            self.away_team = match.group(4)

            self.home_score = self.parse_score(match.group(5))
            self.away_score = self.parse_score(match.group(6))
            self.event_type = match.group(7)
            self.key = "{} {}".format(self.entry_published, self.entry_summary)

        else:
            raise Exception("Failed to parse {}".format(self.entry_summary))

    def parse_score(self, text):
        if text == '':
            return None
        else:
            return int(text)


def __str__(self):
    return "{} {}".format(self.entry_published, self.entry_summary)


class SportballEventFilter(object):
    def __init__(self, rules):
        self.rules = rules
        self.event_keys = set()

    def process_event(self, event):
        is_new_event = event.key not in self.event_keys
        if is_new_event:
            print(event.entry_summary)
            for rule in self.rules:
                rule.process_event(event)

            self.event_keys.add(event.key)


class TeamColours(object):
    pass


class Rule(object):
    def __init__(self, my_team_name, my_team_colours, not_my_team_colours, lights, display):
        self.lights = lights
        self.my_team_name = my_team_name
        self.my_team_scored_goal_event_type = "Goal for {}".format(self.my_team_name)
        self.whistle_colour = (8, 8, 8)
        self.my_team_colours = my_team_colours
        self.not_my_team_colours = not_my_team_colours
        self.display = display

    def process_event(self, event):

        if self.team_name_match(event):
            self._display(event)

            colours = TeamColours()

            my_team_is_home_team = event.home_team == self.my_team_name
            if my_team_is_home_team:
                colours.home_team_colours = self.my_team_colours
                colours.away_team_colours = self.not_my_team_colours
            else:
                colours.home_team_colours = self.not_my_team_colours
                colours.away_team_colours = self.my_team_colours

            if event.event_type.startswith("Goal for"):
                if event.event_type == self.my_team_scored_goal_event_type:
                    self.on_scored_a_goal(event, colours)
                else:
                    self.on_conceded_a_goal(event, colours)
            elif event.event_type == "Kick Off":
                self.whistle(".")
            elif event.event_type == "2nd Half Started":
                self.whistle(".")
            elif event.event_type == "Halftime":
                self.on_half_time(event, colours)
            elif event.event_type == "Match Finished":
                self.on_full_time(event, colours)
            elif event.event_type == "Match Postponed":
                pass
            else:
                raise Exception("Unknown event type {}".format(event.event_type))

    def _display(self, event):
        if self.display:
            self.display.show(event.entry_summary)

    def team_name_match(self, event):
        return self.my_team_name in event.home_team or self.my_team_name in event.away_team

    def on_scored_a_goal(self, event, colours):
        print(event)
        self.whistle(".")
        self.gooooooaaaaaalllllll(self.my_team_colours)
        # self.whistle(".")
        # self.scores(event, colours)

    def on_conceded_a_goal(self, event, colours):
        print(event)
        self.whistle(".")
        self.gooooooaaaaaalllllll(self.not_my_team_colours)
        # self.whistle(".")
        # self.scores(event, colours)

    def on_half_time(self, event, colours):
        print(event)
        self.whistle(".-")
        self.scores(event, colours)

    def on_full_time(self, event, colours):
        print(event)
        self.whistle("..-")
        self.scores(event, colours)

    def _lights(self, pattern, colour):
        for light in self.lights:
            light.display(pattern, colour)

    def whistle(self, pattern):
        self._lights(pattern, self.whistle_colour)

    def gooooooaaaaaalllllll(self, colours):
        self._lights("!", colours)

    def scores(self, event, colours):
        if event.home_score == 0:
            self._pause("-")
        else:
            self._lights("." * event.home_score, colours.home_team_colours[0])
        # self.whistle(".")
        if event.away_score == 0:
            self._pause("-")
        else:
            self._lights("." * event.away_score, colours.away_team_colours[0])
        # self.whistle(".")

    def _pause(self, param):
        time.sleep(1)


bright = 255


class Leeds(Rule):
    def __init__(self, lights, display):
        super(Leeds, self).__init__(
            "Leeds",
            [(0, 0, bright), (bright, bright, 0)],
            [(bright, 0, 0), (0, bright, bright)],
            lights,
            display
        )


class AllTheThings(Rule):
    def __init__(self, lights, display):
        super(AllTheThings, self).__init__(
            None,
            [(0, bright, 0), (0, bright, bright)],
            [(bright, 0, 0), (bright, 0, bright)],
            lights,
            display
        )

    def team_name_match(self, event):
        return True


def update():
    # hack to prevent bozo errors
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    print("Updating {}".format(datetime.datetime.now()))
    feed = feedparser.parse(feed_url)
    # pprint.pprint(feed)
    entries = feed['entries']
    # print("Received {} entries".format(len(entries)))
    entries.reverse()
    for entry in entries:
        # print(entry['summary'])
        event = SportballEvent(entry)
        event_filter.process_event(event)
    print("Updated {}".format(datetime.datetime.now()))


class Lights(object):
    def display(self, pattern, colour):
        print("{} {}".format(pattern, colour))

    def off(self):
        print("off")


class ConsoleLights(Lights):
    def display(self, pattern, colour):
        print("{} {}".format(pattern, colour))

    def off(self):
        print("off")


class BlinkstickLights(Lights):
    def __init__(self, blinkstick_helper):
        self._bs = blinkstick_helper

    def display(self, pattern, colour):
        self._bs.off()
        time.sleep(0.5)  # gap between chars
        for char in pattern:
            if char == " ":
                self._bs.off()
                time.sleep(1)
            elif char == ".":
                print("dot")
                self._bs.all(colour)
                time.sleep(0.5)
            elif char == "-":
                print("dash")
                self._bs.all(colour)
                time.sleep(2)
            elif char == "!":
                print("exclamation")
                for _ in range(5):
                    for c in colour:
                        self._bs.all(c)
                        time.sleep(0.5)
            self._bs.off()
            time.sleep(0.5)  # gap between chars
        time.sleep(0.5)  # gap between patterns

    def off(self):
        self._bs.off()


class HueLightsAdapter(Lights):
    def __init__(self, hue_wrapper):
        self._state = {}
        self._hue = hue_wrapper

    def display(self, pattern, colour):
        self.save_state()

        self._hue.off()
        time.sleep(0.5)  # gap between patterns

        for char in pattern:
            if char == " ":
                time.sleep(1)
            elif char == ".":
                print("dot")
                hsv = rgb_to_hsv(*colour)
                self._hue.set_hsv(*hsv)
                self._hue.on()
                time.sleep(0.5)
            elif char == "-":
                print("dash")
                hsv = rgb_to_hsv(*colour)
                self._hue.set_hsv(*hsv)
                self._hue.on()
                time.sleep(2)
            elif char == "!":
                print("exclamation")
                for c in colour:
                    hsv = rgb_to_hsv(*c)
                    self._hue.set_hsv(*hsv)
                    self._hue.on()
                    time.sleep(0.5)
            self._hue.off()
            time.sleep(0.5)  # gap between chars
        time.sleep(0.5)  # gap between patterns
        self.recall_state()

    def off(self):
        self._hue.off()

    def save_state(self):
        print("Saving state")
        pprint.pprint(self._hue.light.__dict__)
        self._state["on"] = self._hue.light.on
        # pprint.pprint(self._state)

    def recall_state(self):
        print("Recalling state")
        pprint.pprint(self._state)
        self._hue.light.on = self._state["on"]


def _init_blinksticks(lights):
    blinksticks = blinkstick.find_all()
    for bstick in blinksticks:
        description = bstick.get_description()
        print(bstick.get_serial(), description)
        if description == "BlinkStick Nano":
            blinkstick_nano = BlinkstickLights(BlinkstickNanoWrapper())
            lights.append(blinkstick_nano)
        elif description == "BlinkStick Flex":
            blinkstick_flex = BlinkstickLights(BlinkstickFlexWrapper())
            lights.append(blinkstick_flex)
        else:
            print("UNKNOWN {}".format(description))


event_filter = None


def _init_hue(lights):
    hue = HueWrapper()
    hue.connect()
    hue.quick_transitions()
    lights.append(HueLightsAdapter(hue))
    hue.on()
    hue.brightness(254)


if __name__ == '__main__':
    lights = [
        ConsoleLights(),
    ]

    _init_blinksticks(lights)
    # _init_hue(lights)
    display = ScrollHatWrapper()
    rules = [
        Leeds(lights, display),
        AllTheThings(lights, display)
    ]
    event_filter = SportballEventFilter(rules)

    scheduler = BlockingScheduler()
    scheduler.add_job(update, IntervalTrigger(minutes=1))
    scheduler.add_job(display.scroll)

    try:
        update()
        scheduler.start()
    except KeyboardInterrupt:
        pass
    finally:
        if scheduler.running:
            scheduler.shutdown()
        for light in lights:
            light.off()
