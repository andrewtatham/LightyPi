import random

from cube import cube_helper


class Pixel(object):
    def __init__(self, xyz):
        self.xyz = xyz


class SnakeSegment(Pixel):
    pass


class SnakeHead(SnakeSegment):
    pass


class Snake(object):
    def __init__(self, cube):
        self.cube = cube
        self.segments = []
        self.length = 2
        self.rgb = cube_helper.get_random_rgb()
        self.alive = True
        self.xyz = cube_helper.start_position(self.cube.n)
        self.direction = cube_helper.get_random_direction()

    def clear(self):
        pass

    def update(self):
        # Move

        # grow
        if len(self.segments) < self.length:
            segment = SnakeSegment()
            self.segments.append(segment)

        pass

    def draw(self):
        pass


class SnakeFactory(object):
    def __init__(self, cube):
        self.cube = cube

    def create(self):
        snake = Snake(self.cube)
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
        for snake in self.snakes:
            snake.update()
        if random.randint(0, 5) == 0:
            new = self.factory.create()
            self.snakes.append(new)
        for snake in self.snakes:
            snake.draw()
        self.cube.show()
