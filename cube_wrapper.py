import time
import neopixel

# LED strip configuration:
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
        led_count = n * n * n
        self.strip = neopixel.Adafruit_NeoPixel(
            led_count, LED_PIN, LED_FREQ_HZ,
            LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        self.map = None
        self._build_map()
        self.hello()

    def _build_map(self):
        self.map = [[[0 for _ in range(self.n)] for _ in range(self.n)] for _ in range(self.n)]
        led = 0
        for x in range(self.n):
            for y in range(self.n):
                for z in range(self.n):
                    print("[{},{},{}] = {}".format(x, y, z, led))
                    self.map[x][y][z] = led
                    led += 1

    def _unmap(self, xyz):
        x = xyz[0]
        y = xyz[1]
        z = xyz[2]
        led = self.map[x][y][z]
        print("[{}] = {}".format(xyz, led))
        return led

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
        led = self._unmap(xyz)
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        colour = neopixel.Color(r, g, b)
        self.strip.setPixelColor(led, colour)

    def show(self, sleep=0.1):
        self.strip.show()
        time.sleep(sleep)
