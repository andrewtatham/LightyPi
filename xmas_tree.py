from gpiozero import LEDBoard
from gpiozero.tools import random_values, sin_values, scaled
from signal import pause


def random():
    for led in tree:
        led.source_delay = 0.1
        led.source = random_values()


def sin():
    for led in tree:
        led.source_delay = 0.1
        led.source = scaled(sin_values(), 0, 1, -1, 1)


if __name__ == '__main__':
    tree = LEDBoard(*range(2, 28), pwm=True)
    # random()
    sin()
    pause()
