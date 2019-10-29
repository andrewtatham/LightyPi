import random

from helper import colour_helper
from cube_wrapper import cube_helper


class Snake(object):
    def __init__(self, cube, length, rgb, rgb_alt, xyz, direction):
        self.cube = cube
        self.segments = []

    def clear(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class SnakeFactory(object):
    def __init__(self, cube):
        self.cube = cube

    def create(self):
        length = 2
        rgb = colour_helper.get_random_rgb()
        rgb_alt = rgb
        xyz = cube_helper.start_position(self.cube.n)
        direction = None
        snake = Snake(self.cube, length, rgb, rgb_alt, xyz, direction)
        return snake


class SnakeGame(object):
    def __init__(self, cube):
        self.cube = cube
        self.snakes = []
        self.factory = SnakeFactory(cube)
        for _ in range(2):
            new = self.factory.create()
            self.snakes.append(new)

    def run(self):
        for snake in self.snakes:
            snake.clear()
        for snakes in self.snakes:
            snake.update()
        if random.randint(0, 5) == 0:
            new = self.factory.create()
            self.snakes.append(new)
        for snake in self.snakes:
            snake.draw()
        self.cube.show()
