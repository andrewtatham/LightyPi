import datetime
import time
import re

from blinkstick import blinkstick
import feedparser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from blinkstick_flex_wrapper import BlinkstickFlexWrapper
from blinkstick_nano_wrapper import BlinkstickNanoWrapper

feed_url = "https://www.scorespro.com/rss2/live-soccer.xml"
rx = re.compile("^\((\w*)-(\w*)\) (.*) vs (.*): (\d*)-(\d*) - (.*)$", re.MULTILINE)


class SportballEvent(object):
    def __init__(self, entry):
        self.entry_summary = entry['summary']
        self.entry_published = entry["published"]
        match = rx.match(self.entry_summary)
        if match:
            self.country = match.group(1)
            self.league = match.group(2)
            self.home_team = match.group(3)
            self.away_team = match.group(4)
            self.home_score = match.group(5)
            self.away_score = match.group(6)
            self.event_type = match.group(7)
            self.key = "{} {}".format(self.entry_published, self.entry_summary)
        else:
            raise Exception("Failed to parse ()".format(self.entry_summary))

    def __str__(self):
        return "{} {}".format(self.entry_published, self.entry_summary)


class SportballEventFilter(object):
    def __init__(self, rules):
        self.rules = rules
        self.event_keys = set()

    def process_event(self, event):
        is_new_event = event.key not in self.event_keys
        if is_new_event:
            for rule in self.rules:
                rule.process_event(event)

            self.event_keys.add(event.key)


class TeamColours(object):
    pass


class Rule(object):
    def __init__(self, my_team_name, my_team_colours, not_my_team_colours, lights):
        self.lights = lights
        self.my_team_name = my_team_name
        self.my_team_scored_goal_event_type = "Goal for {}".format(self.my_team_name)
        self.whistle_colour = (8, 8, 8)
        self.my_team_colours = my_team_colours
        self.not_my_team_colours = not_my_team_colours

    def process_event(self, event):

        if self.team_name_match(event):

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
                pass
            elif event.event_type == "2nd Half Started":
                pass
            elif event.event_type == "Halftime":
                self.on_half_time(event, colours)
            elif event.event_type == "Match Finished":
                self.on_full_time(event, colours)
            else:
                raise Exception("Unknown event type {}".format(event.event_type))

    def team_name_match(self, event):
        return self.my_team_name in event.home_team or self.my_team_name in event.away_team

    def on_scored_a_goal(self, event, colours):
        print(event)
        self.whistle("-")
        self.gooooooaaaaaalllllll(self.my_team_colours)
        self.whistle(".")
        self.scores(event, colours)

    def on_conceded_a_goal(self, event, colours):
        print(event)
        self.whistle("-")
        self.gooooooaaaaaalllllll(self.not_my_team_colours)
        self.whistle(".")
        self.scores(event, colours)

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
        for _ in range(5):
            for colour in colours:
                self._lights(".", colour)

    def scores(self, event, colours):

        if event.home_score == 0:
            self._pause("-")
        else:
            for _ in event.home_score:
                for colour in colours.home_team_colours:
                    self._lights(".", colour)
                self._pause(".")
            self._pause("-")

        if event.away_score == 0:
            self._pause("-")
        else:
            for _ in event.away_score:
                for colour in colours.away_team_colours:
                    self._lights(".", colour)
                self._pause(".")
            self._pause("-")

    def _pause(self, param):
        time.sleep(1)


class Leeds(Rule):
    def __init__(self, lights):
        super(Leeds, self).__init__(
            "Leeds",
            [(8, 8, 0), (0, 0, 8)],
            [(8, 0, 0), (0, 8, 8)],
            lights
        )


class AllTheThings(Rule):
    def __init__(self, lights):
        super(AllTheThings, self).__init__(
            None,
            [(8, 8, 0), (0, 0, 8)],
            [(8, 0, 0), (0, 8, 8)],
            lights
        )

    def team_name_match(self, event):
        return True


def update():
    print(datetime.datetime.now())
    feed = feedparser.parse(feed_url)
    entries = feed['entries']
    entries.reverse()
    for entry in entries:
        # print(entry['summary'])
        event = SportballEvent(entry)
        event_filter.process_event(event)

class Lights(object):
    pass

class ConsoleLights(Lights):
    def display(self, pattern, colour):
        print("{} {}".format(pattern, colour))


class BlinkstickLights(Lights):
    def __init__(self, blinkstick_helper):
        self._bs = blinkstick_helper

    def display(self, pattern, colour):
        for char in pattern:
            if char == " ":
                self._bs.off()
                time.sleep(1)
            elif char == ".":
                self._bs.all(colour)
            elif char == "-":
                self._bs.all(colour)
                time.sleep(1)


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



if __name__ == '__main__':
    lights = [
        ConsoleLights(),
    ]

    _init_blinksticks(lights)

    rules = [
        Leeds(lights),
        AllTheThings(lights)
    ]
    event_filter = SportballEventFilter(rules)

    scheduler = BlockingScheduler()
    scheduler.add_job(update, IntervalTrigger(minutes=15))

    try:
        update()
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()
    finally:
        pass
