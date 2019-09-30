from helper import colour_helper

if __name__ == '__main__':

    for i in range(12):
        h = i / 12
        s = 1.0
        v = 255
        hsv = (h, s, v)
        rgb = colour_helper.hsv_to_rgb(hsv)
        print("F{} {}".format(i + 1, rgb))
