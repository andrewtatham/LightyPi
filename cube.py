import logging
import platform
import random
import time


def get_random_colour():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

_platform = platform.platform()
node = platform.node()
logger.info("platform: %s", _platform)
logger.info("node: %s", node)
is_windows = _platform.startswith('Windows')
is_mac_osx = _platform.startswith('Darwin')
is_linux = _platform.startswith('Linux')
is_rpi = node == "phatstack"
is_viz = not is_rpi
n = 5
cube = None
if not is_viz:
    logger.info("Cube")
    import cube_wrapper

    cube = cube_wrapper.Cube(n)
else:
    logger.info("Viz")
    import cube_visualiser

    cube = cube_visualiser.Cube(n)


def sleep(secs):
    if not is_viz:
        time.sleep(secs)


def hello():
    b = 255
    set_all_rgb((b, 0, 0), "x")
    sleep(1)
    set_all_rgb((0, b, 0), "y")
    sleep(1)
    set_all_rgb((0, 0, b), "z")
    sleep(1)
    off()
    sleep(1)
    set_all_rgb((b, b, b))
    sleep(0.1)
    off()
    sleep(1)


def off():
    set_all_rgb((0, 0, 0))


def set_all_rgb(rgb, by=None):
    bys = {
        "x": lambda ijk: (i, j, k),
        "y": lambda ijk: (k, i, j),
        "z": lambda ijk: (j, k, i),
    }
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if by:
                    xyz = bys[by]((i, j, k))
                else:
                    xyz = (i, j, k)
                cube.set_rgb(xyz, rgb)
        if by:
            cube.show()
            sleep(0.2)
    if not by:
        cube.show()


try:
    run = True
    t = 0

    hello()

    while run:
        for i in range(n):
            rgb = get_random_colour()
            for j in range(n):
                for k in range(n):
                    xyz = (i, j, k)
                    cube.set_rgb(xyz, rgb)
        cube.show()

        if not is_viz:
            sleep(1)
        else:
            t += 1
            if t > 10:
                run = False
except KeyboardInterrupt:
    pass
finally:
    off()

if is_viz:
    cube.show_me_what_you_got()
