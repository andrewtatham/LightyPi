import logging
import platform

from cube_stuff import cube_helper
from cube_stuff.bouncy_ball import BouncyBalls
from cube_stuff.starfield import StarField
from cube_stuff.wavey import WaveGame

# from cube_stuff.snake_3d import SnakeGame

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

on_secs = 12
off_secs = 1


class CubeWrapper(object):
    def __init__(self, n, cube_instance):
        self.n = n
        self._cube_instance = cube_instance
        self._run = True

    def _hello(self):
        b = 255
        self._set_all_rgb((b, 0, 0), "x")
        self._sleep(2)
        self._set_all_rgb((0, b, 0), "y")
        self._sleep(2)
        self._set_all_rgb((0, 0, b), "z")
        self._sleep(2)
        self._off()

    def _rgb_cube(self):
        bright = 255
        for x in range(self.n):
            for y in range(self.n):
                for z in range(self.n):
                    r = int(x * bright / self.n)
                    g = int(y * bright / self.n)
                    b = int(z * bright / self.n)
                    self._cube_instance.set_rgb((x, y, z), (r, g, b))
        self._cube_instance.show()

    def _hsv_cube(self):
        for x in range(self.n):
            for y in range(self.n):
                for z in range(self.n):
                    h = 1.0 * x / self.n
                    s = 1.0 * y / self.n
                    v = 255 * z / self.n
                    rgb = cube_helper.hsv_to_rgb((h, s, v))
                    self._cube_instance.set_rgb((x, y, z), rgb)
        self._cube_instance.show()

    def _rainbow_cube(self):
        s = 1.0
        v = 255
        for x in range(self.n):
            h = 1.0 * x / self.n
            for y in range(self.n):
                for z in range(self.n):
                    rgb = cube_helper.hsv_to_rgb((h, s, v))
                    self._cube_instance.set_rgb((x, y, z), rgb)
        self._cube_instance.show()

    def _off(self):
        self._set_all_rgb((0, 0, 0))

    def _sleep(self, secs):
        self._cube_instance.sleep(secs)

    def _sleep_off_sleep(self, secs_before, secs_after):
        self._sleep(secs_before)
        self._off()
        self._sleep(secs_after)

    def _off_sleep(self, secs):
        self._off()
        self._sleep(secs)

    def _show_sleep(self, secs):
        self._cube_instance.show()
        self._sleep(secs)

    def _set_all_rgb(self, rgb, by=None):
        if not by:
            by = "z"
        map_func = cube_helper.bys[by]

        for i in range(self.n):
            for j in range(self.n):
                for k in range(self.n):
                    xyz = map_func((i, j, k))
                    self._cube_instance.set_rgb(xyz, rgb)
            if by:
                self._cube_instance.show()
                self._sleep(0.2)
        if not by:
            self._cube_instance.show()

    def _snake(self):
        game = SnakeGame(self._cube_instance)
        while game.run():
            pass
        self._off()

    def _starfield(self):
        game = StarField(self._cube_instance)
        for _ in range(100):
            game.run()
            self._sleep(0.1)
        self._off()

    def _bouncy_ball(self):
        game = BouncyBalls(self._cube_instance)
        for _ in range(100):
            game.run()
            self._sleep(0.05)
        self._off()

    def _wavey(self):
        game = WaveGame(self._cube_instance)
        for _ in range(100):
            game.run()
            self._sleep(0.05)
        self._off()

    def run(self, n=0):
        try:
            self._run = True
            t = 0

            while self._run:
                self._hello()
                self._sleep_off_sleep(on_secs, off_secs)

                self._rgb_cube()
                self._sleep_off_sleep(on_secs, off_secs)

                self._hsv_cube()
                self._sleep_off_sleep(on_secs, off_secs)

                self._rainbow_cube()
                self._sleep_off_sleep(on_secs, off_secs)

                self._bouncy_ball()

                # self._snake()

                self._starfield()

                self._wavey()

                if n:
                    t += 1
                    if t >= n:
                        self._run = False

        except KeyboardInterrupt:
            pass
        finally:
            self._cube_instance.finished()

    def on(self):
        self._run = True

    def off(self):
        self._run = False


def get():
    n = 5
    _platform = platform.platform()
    node = platform.node()
    logger.info("platform: %s", _platform)
    logger.info("node: %s", node)
    is_windows = _platform.startswith('Windows')
    is_mac_osx = _platform.startswith('Darwin')
    # is_linux = _platform.startswith('Linux')
    is_picube = node == "picube"
    cube_instance = None

    if is_windows or is_mac_osx:
        logger.info("Viz")
        from cube_stuff import cube_visualiser
        cube_instance = cube_visualiser.CubeVisualizer(n)
    elif is_picube:
        logger.info("Cube")
        from cube_stuff import cube_actual
        cube_instance = cube_actual.ActualCube(n)

    if cube_instance:
        return CubeWrapper(n, cube_instance)
    else:
        return None


if __name__ == '__main__':
    cube_wrapper = get()
    cube_wrapper.run(1)
