from gpiozero import LEDBoard
from gpiozero.tools import random_values, sin_values
from signal import pause


def random():
    for led in tree:
        led.source_delay = 0.1
        led.source = random_values()


def sin():
    for led in tree:
        led.source_delay = 0.1
        led.source = sin_values()


if __name__ == '__main__':
    tree = LEDBoard(*range(2, 28), pwm=True)
    # random()
    sin()
    pause()
