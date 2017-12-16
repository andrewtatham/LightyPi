from blinkstick_helper import BlinkstickHelper


class BlinkstickNanoWrapper(BlinkstickHelper):
    def __init__(self, led_count=2, serial="BS003518-3.0"):
        BlinkstickHelper.__init__(self, led_count, serial)


if __name__ == '__main__':
    bs = BlinkstickNanoWrapper()
    try:
        bs.hello()
        bs.xmas()
    except KeyboardInterrupt:
        pass
    finally:
        bs.off()
