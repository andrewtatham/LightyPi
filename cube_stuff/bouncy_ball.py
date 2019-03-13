import operator
import random

from cube_stuff import cube_helper


class Ball(object):
    def __init__(self, xyz, rgb, velocity_xyz, cube):
        self.velocity_xyz = velocity_xyz
        self.rgb = rgb
        self.xyz = xyz
        self.cube = cube

    def clear(self):
        self.cube.set_rgb(self.xyz, cube_helper.rgb_black)

    def update(self):
        if cube_helper.is_at_edge(self.xyz, self.cube.n):
            # print("before bounce: {} + {}".format(self.xyz, self.velocity_xyz))
            self.xyz, self.velocity_xyz = cube_helper.bounce(self.xyz, self.velocity_xyz, self.cube.n)
            # print("after bounce: {} + {}".format(self.xyz, self.velocity_xyz))
        self.xyz = tuple(map(operator.add, self.xyz, self.velocity_xyz))
        # print("updated: {}".format(self.xyz))

    def draw(self):
        self.cube.set_rgb(self.xyz, self.rgb)


class BallFactory(object):
    def __init__(self, cube):
        self.cube = cube

    def create(self):
        rgb = cube_helper.get_random_rgb()
        xyz = cube_helper.start_position(self.cube.n)
        velocity_xyz = cube_helper.velocity_xyz()
        ball = Ball(xyz, rgb, velocity_xyz, self.cube)
        return ball


class BouncyBalls(object):
    def __init__(self, cube):
        self.cube = cube
        self.balls = []
        self.factory = BallFactory(cube)
        for _ in range(2):
            new = self.factory.create()
            self.balls.append(new)

    def run(self):
        for ball in self.balls:
            ball.clear()
        for ball in self.balls:
            ball.update()
        if random.randint(0, 5) == 0:
            new = self.factory.create()
            self.balls.append(new)
        for ball in self.balls:
            ball.draw()
        self.cube.show()
