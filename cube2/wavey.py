import math
import random

import cube_helper


class Wave(object):
    def __init__(self, cube, i, rgb):
        self.cube = cube
        self.segments = [0 for _ in range(self.cube.n)]
        self.t = 0
        self.i = i
        self.rgb = rgb

    def clear(self):
        for j in range(self.cube.n):
            k = self.segments[j]
            xyz = (self.i, j, k)
            self.cube.set_rgb(xyz, cube_helper.rgb_black)

    def update(self):
        self.t += 1
        for j in range(self.cube.n):
            degrees = self.t * 15.0 + self.i * 90.0 + j * 45.0
            radians = degrees * math.pi / 180.0
            factor = -0.5 + 0.5 * math.sin(radians)
            k = int(self.cube.n * factor)
            self.segments[j] = k

    def draw(self):
        for j in range(self.cube.n):
            k = self.segments[j]
            xyz = (self.i, j, k)
            self.cube.set_rgb(xyz, self.rgb)


class WaveFactory(object):
    def __init__(self, cube):
        self.cube = cube

    def create(self, n):
        waves = []
        h_delta = random.uniform(0.05, 0.35)
        hsv = cube_helper.get_random_hsv()
        for i in range(n):
            hsv = cube_helper.h_delta(hsv, h_delta)
            rgb = cube_helper.hsv_to_rgb(hsv)
            wave = Wave(self.cube, i, rgb)
            waves.append(wave)
        return waves


class WaveGame(object):
    def __init__(self, cube):
        self.cube = cube
        self.waves = []
        self.factory = WaveFactory(cube)
        new = self.factory.create(5)
        self.waves.extend(new)

    def run(self):
        for wave in self.waves:
            wave.clear()
        for wave in self.waves:
            wave.update()
        for wave in self.waves:
            wave.draw()
        self.cube.show()
