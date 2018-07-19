import logging
import platform
import random
import time

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
i = 0
while run:
    for x in range(n):
        for y in range(n):
            for z in range(n):
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)

                rgb = (r, g, b)
                xyz = (x, y, z)
                cube.set_rgb(xyz, rgb)
    cube.show()

    if is_linux:
        time.sleep(1)
    else:
        i += 1
        if i > 10:
            run = False

if not is_linux:
    cube.show_me_what_you_got()
