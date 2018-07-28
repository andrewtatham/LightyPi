import random

import cube_helper


class Star(object):
    def __init__(self, xyz, rgb, direction_func, cube):
        self.direction_func = direction_func
        self.rgb = rgb
        self.xyz = xyz
        self.cube = cube
        self.alive = True

    def clear(self):
        self.cube.set_rgb(self.xyz, cube_helper.rgb_black)

    def update(self):
        self.xyz = self.direction_func(self.xyz)
        self.alive = not cube_helper.is_out_of_bounds(self.xyz, self.cube.n)

    def draw(self):
        self.cube.set_rgb(self.xyz, self.rgb)


class StarFactory(object):
    def __init__(self, cube):
        self.cube = cube
        self.rgb = random.choice([
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255)
        ])
        self.direction_func = cube_helper.direction_funcs["x+"]

    def create(self):
        x = 0
        y = random.randint(0, self.cube.n - 1)
        z = random.randint(0, self.cube.n - 1)
        xyz = x, y, z
        star = Star(xyz, self.rgb, self.direction_func, self.cube)
        return star


class StarField(object):
    def __init__(self, cube):
        self.cube = cube
        self.stars = []
        self.factory = StarFactory(cube)

    def run(self):
        for star in self.stars:
            star.clear()
        for star in self.stars:
            star.update()
        dead_stars = list(filter(lambda s: not s.alive, self.stars))
        if any(dead_stars):
            for dead_star in dead_stars:
                self.stars.remove(dead_star)
        for _ in range(2):
            self.stars.append(self.factory.create())
        for star in self.stars:
            star.draw()
        self.cube.show()
