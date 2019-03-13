import math
import random

from cube_stuff import cube_helper


class Wave(object):
    def __init__(self, cube, rgb, map_func):
        self.cube = cube
        self.segments = [[0 for _ in range(self.cube.n)] for _ in range(self.cube.n)]
        self.t = 0
        self.rgb = rgb
        self.map_func = map_func
        self.t_phase = random.randint(-180, 180) / self.cube.n
        self.i_phase = random.randint(-180, 180) / self.cube.n
        self.j_phase = random.randint(-180, 180) / self.cube.n
        # print("t_phase:{} i_phase:{} j_phase:{}".format(self.t_phase, self.i_phase, self.j_phase))

    def clear(self):
        for i in range(self.cube.n):
            for j in range(self.cube.n):
                k = self.segments[i][j]
                xyz = self.map_func((i, j, k))
                self.cube.set_rgb(xyz, cube_helper.rgb_black)

    def update(self):
        self.t += 1
        for i in range(self.cube.n):
            for j in range(self.cube.n):
                degrees = (self.t * self.t_phase + i * self.i_phase + j * self.j_phase) % 360
                radians = degrees * math.pi / 180.0
                factor = 0.5 + 0.5 * math.sin(radians)
                k = int(round((self.cube.n - 1) * factor))
                # print("t:{} i:{} j:{} degrees:{} radians:{} factor:{} k:{}"
                #       .format(self.t, self.i, j, degrees, radians, factor, k))
                self.segments[i][j] = k

    def draw(self):
        for i in range(self.cube.n):
            for j in range(self.cube.n):
                k = self.segments[i][j]
                xyz = self.map_func((i, j, k))
                self.cube.set_rgb(xyz, self.rgb)


class WaveFactory(object):
    def __init__(self, cube):
        self.cube = cube

        by = random.choice(list(cube_helper.bys.keys()))
        self.map_func = cube_helper.bys[by]

        self.rgb = cube_helper.get_random_rgb()

    def create(self):
        wave = Wave(self.cube, self.rgb, self.map_func)
        return wave


class WaveGame(object):
    def __init__(self, cube):
        self.cube = cube
        self.waves = []
        self.factory = WaveFactory(cube)
        new = self.factory.create()
        self.waves.append(new)

    def run(self):
        for wave in self.waves:
            wave.clear()
        for wave in self.waves:
            wave.update()
        for wave in self.waves:
            wave.draw()
        self.cube.show()
