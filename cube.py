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
logger.info("platform: %s", _platform)
is_windows = _platform.startswith('Windows')
is_mac_osx = _platform.startswith('Darwin')
is_linux = _platform.startswith('Linux')

n = 5
cube = None
if is_linux:
    import cube_wrapper

    cube = cube_wrapper.Cube(n)
else:
    import cube_visualiser

    cube = cube_visualiser.Cube(n)

run = True
t = 0

try:
    while run:
        for i in range(n):
            rgb = get_random_colour()
            for j in range(n):
                for k in range(n):
                    xyz = (i, j, k)
                    cube.set_rgb(xyz, rgb)
        cube.show()

        if is_linux:
            time.sleep(1)
        else:
            t += 1
            if t > 10:
                run = False
except KeyboardInterrupt:
    pass
finally:
    cube.off()

if not is_linux:
    cube.show_me_what_you_got()
