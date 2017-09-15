from blinkstick_helper import BlinkstickHelper


class BlinkstickFlexWrapper(BlinkstickHelper):
    def __init__(self, led_count=32, serial="BS006639-3.1"):
        BlinkstickHelper.__init__(self, led_count, serial)


if __name__ == '__main__':
    bs = BlinkstickFlexWrapper()
    try:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        bs.off()
