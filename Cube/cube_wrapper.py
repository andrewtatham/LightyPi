import time

import neopixel

# LED strip configuration:
from cube_base import CubeBase
from cube_map import CubeMap

LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 8  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53


class Cube(CubeBase):
    def __init__(self, n):
        self.n = n
        led_count = n * n * n
        self.strip = neopixel.Adafruit_NeoPixel(
            led_count, LED_PIN, LED_FREQ_HZ,
            LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        self.map = CubeMap(n)

    def set_rgb(self, xyz, rgb):
        led = self.map.unmap(xyz)
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        colour = neopixel.Color(g, r, b)
        self.strip.setPixelColor(led, colour)

    def show(self):
        self.strip.show()
