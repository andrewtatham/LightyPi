import time

import neopixel

# LED strip configuration:
from cube_map import CubeMap

LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 8  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53


class Cube(object):
    def __init__(self, n):
        self.n = n
        self.n2 = n * n
        self.n3 = n * n * n
        led_count = self.n3
        self.strip = neopixel.Adafruit_NeoPixel(
            led_count, LED_PIN, LED_FREQ_HZ,
            LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        self.map = CubeMap(5)
        self.hello()

    def set_all_rgb(self, rgb):
        for x in range(self.n):
            for y in range(self.n):
                for z in range(self.n):
                    xyz = (x, y, z)
                    self.set_rgb(xyz, rgb)
                    self.show()

    def hello(self):
        b = 255
        self.set_all_rgb((b, 0, 0))
        self.set_all_rgb((0, b, 0))
        self.set_all_rgb((0, 0, b))
        self.off()

    def off(self):
        self.set_all_rgb((0, 0, 0))

    def set_rgb(self, xyz, rgb):
        led = self.map.unmap(xyz)
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        colour = neopixel.Color(r, g, b)
        self.strip.setPixelColor(led, colour)

    def show(self):
        self.strip.show()



