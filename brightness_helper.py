day_factor = None
brightness = None
v = None


def set_day_factor(_day_factor):
    global day_factor, brightness, v
    day_factor = _day_factor
    brightness = int(8 + 64 * day_factor)
    v = brightness


set_day_factor(1.0)
