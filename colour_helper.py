import colorsys
import datetime
import random

rgb_black = (0, 0, 0)


def get_random_hsv():
    h = random.uniform(0.0, 1.0)
    s = 1.0
    v = brightness
    return h, s, v


def get_random_rgb():
    return hsv_to_rgb(get_random_hsv())


def h_delta(hsv, h_delta):
    h, s, v = hsv
    h = (h + h_delta) % 1.0
    return h, s, v


def hsv_to_rgb(hsv):
    h = hsv[0]
    s = hsv[1]
    v = hsv[2]
    rgb = colorsys.hsv_to_rgb(h, s, v)
    r = int(rgb[0])
    g = int(rgb[1])
    b = int(rgb[2])
    return r, g, b


def get_day_factor(from_dt, now_dt, to_dt, increasing):
    if increasing and now_dt >= to_dt or not increasing and now_dt <= from_dt:
        return 1.0
    elif increasing and now_dt <= from_dt or not increasing and now_dt >= to_dt:
        return 0.0
    else:
        x = now_dt - from_dt
        y = to_dt - from_dt
        day_factor = x.total_seconds() / y.total_seconds()
        if increasing:
            return day_factor
        else:
            return 1.0 - day_factor


def set_day_factor(_day_factor):
    global day_factor, brightness
    day_factor = _day_factor
    brightness = int(8 + 64 * day_factor)


day_factor = None
brightness = None

if __name__ == '__main__':
    from_dt = datetime.datetime(2019, 3, 15, 6, 0)
    to_dt = datetime.datetime(2019, 3, 15, 9, 0)
    range_minutes = (to_dt - from_dt).seconds / 60
    step_minutes = 15

    date_generated = (from_dt + datetime.timedelta(minutes=mins) for mins in
                      range(-30, range_minutes + 30, step_minutes))

    for now_dt in date_generated:
        sunrise = get_day_factor(from_dt, now_dt, to_dt, True)
        sunset = get_day_factor(from_dt, now_dt, to_dt, False)
        print ("{} {} {}".format(now_dt, sunrise, sunset))
