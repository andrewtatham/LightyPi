import logging
import platform
import time

import cube_helper
from bouncy_ball import BouncyBalls
# import snake_3d
from starfield import StarField
from wavey import WaveGame

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

_platform = platform.platform()
node = platform.node()
logger.info("platform: %s", _platform)
logger.info("node: %s", node)
is_windows = _platform.startswith('Windows')
is_mac_osx = _platform.startswith('Darwin')
is_linux = _platform.startswith('Linux')
is_rpi = node == "picube"
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


def hello():
    b = 255
    set_all_rgb((b, 0, 0), "x")
    sleep(2)
    set_all_rgb((0, b, 0), "y")
    sleep(2)
    set_all_rgb((0, 0, b), "z")
    sleep(2)
    off()


def rgb_cube():
    bright = 255
    for x in range(n):
        for y in range(n):
            for z in range(n):
                r = int(x * bright / n)
                g = int(y * bright / n)
                b = int(z * bright / n)
                cube.set_rgb((x, y, z), (r, g, b))
    cube.show()


def hsv_cube():
    for x in range(n):
        for y in range(n):
            for z in range(n):
                h = 1.0 * x / n
                s = 1.0 * y / n
                v = 255 * z / n
                rgb = cube_helper.hsv_to_rgb((h, s, v))
                cube.set_rgb((x, y, z), rgb)
    cube.show()


def rainbow_cube():
    s = 1.0
    v = 255
    for x in range(n):
        h = 1.0 * x / n
        for y in range(n):
            for z in range(n):
                rgb = cube_helper.hsv_to_rgb((h, s, v))
                cube.set_rgb((x, y, z), rgb)
    cube.show()


def off():
    set_all_rgb((0, 0, 0))


def sleep(secs):
    if not is_viz:
        time.sleep(secs)


def sleep_off_sleep(secs_before, secs_after):
    sleep(secs_before)
    off()
    sleep(secs_after)


def off_sleep(secs):
    off()
    sleep(secs)


def show_sleep(secs):
    cube.show()
    sleep(secs)


def set_all_rgb(rgb, by=None):
    if not by:
        by = "z"
    map_func = cube_helper.bys[by]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                xyz = map_func((i, j, k))
                cube.set_rgb(xyz, rgb)
        if by:
            cube.show()
            sleep(0.2)
    if not by:
        cube.show()


on_secs = 12
off_secs = 1

#
# def snake():
#     game = snake_3d.SnakeGame(cube)
#     while game.run():
#         pass
#     off()


def starfield():
    game = StarField(cube)
    for _ in range(100):
        game.run()
        sleep(0.1)
    off()


def bouncy_ball():
    game = BouncyBalls(cube)
    for _ in range(100):
        game.run()
        sleep(0.05)
    off()


def wavey():
    game = WaveGame(cube)
    for _ in range(100):
        game.run()
        sleep(0.05)
    off()


try:
    run = True
    t = 0

    while run:
        if not is_viz:
            hello()
            sleep_off_sleep(on_secs, off_secs)

            rgb_cube()
            sleep_off_sleep(on_secs, off_secs)

            hsv_cube()
            sleep_off_sleep(on_secs, off_secs)

            rainbow_cube()
            sleep_off_sleep(on_secs, off_secs)

            bouncy_ball()

        # snake()

        starfield()

        wavey()

        if is_viz:
            t += 1
            if t > 2:
                run = False

except KeyboardInterrupt:
    pass
finally:
    off()

if is_viz:
    cube.show_me_what_you_got()
