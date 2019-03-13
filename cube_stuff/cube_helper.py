import colorsys
import random

rgb_black = (0, 0, 0)


def get_random_hsv():
    h = random.uniform(0.0, 1.0)
    s = 1.0
    v = 255
    return h, s, v


def get_random_rgb():
    return hsv_to_rgb(get_random_hsv())


def h_delta(hsv, h_delta):
    h, s, v = hsv
    h = (h + h_delta) % 1.0
    return h, s, v


bys = {
    "x": lambda ijk: (ijk[0], ijk[1], ijk[2]),
    "y": lambda ijk: (ijk[1], ijk[2], ijk[0]),
    "z": lambda ijk: (ijk[2], ijk[0], ijk[1]),
}
direction_funcs = {
    "x+": lambda xyz: (xyz[0] + 1, xyz[1], xyz[2]),
    "x-": lambda xyz: (xyz[0] - 1, xyz[1], xyz[2]),
    "y+": lambda xyz: (xyz[0], xyz[1] + 1, xyz[2]),
    "y-": lambda xyz: (xyz[0], xyz[1] - 1, xyz[2]),
    "z+": lambda xyz: (xyz[0], xyz[1], xyz[2] + 1),
    "z-": lambda xyz: (xyz[0], xyz[1], xyz[2] - 1),
}
edge_start_position_funcs = {
    "x+": lambda n: (0, random.randint(0, n - 1), random.randint(0, n - 1)),
    "x-": lambda n: (n - 1, random.randint(0, n - 1), random.randint(0, n - 1)),
    "y+": lambda n: (random.randint(0, n - 1), 0, random.randint(0, n - 1)),
    "y-": lambda n: (random.randint(0, n - 1), n - 1, random.randint(0, n - 1)),
    "z+": lambda n: (random.randint(0, n - 1), random.randint(0, n - 1), 0),
    "z-": lambda n: (random.randint(0, n - 1), random.randint(0, n - 1), n - 1),
}


def start_position(n):
    return random.randint(0, n - 1), random.randint(0, n - 1), random.randint(0, n - 1)


def velocity_xyz():
    x, y, z = 0, 0, 0
    while x == 0:
        x = random.randint(-1, +1)
    while y == 0:
        y = random.randint(-1, +1)
    while z == 0:
        z = random.randint(-1, +1)
    return x, y, z


def is_at_edge(xyz, n):
    x, y, z = xyz
    return x <= 0 or x >= n - 1 or \
           y <= 0 or y >= n - 1 or \
           z <= 0 or z >= n - 1


def is_out_of_bounds(xyz, n):
    x, y, z = xyz
    return x < 0 or x >= n or \
           y < 0 or y >= n or \
           z < 0 or z >= n


def hsv_to_rgb(hsv):
    h = hsv[0]
    s = hsv[1]
    v = hsv[2]
    rgb = colorsys.hsv_to_rgb(h, s, v)
    r = int(rgb[0])
    g = int(rgb[1])
    b = int(rgb[2])
    return r, g, b


def bounce(xyz, velocity_xyz, n):
    x, y, z = xyz
    vx, vy, vz = velocity_xyz

    if x <= 0 and vx < 0:
        x = 0
        vx = -vx
    if x >= n - 1 and vx > 0:
        x = n - 1
        vx = -vx

    if y <= 0 and vy < 0:
        y = 0
        vy = -vy
    if y >= n - 1 and vy > 0:
        y = n - 1
        vy = -vy

    if z <= 0 and vz < 0:
        z = 0
        vz = -vz
    if z >= n - 1 and vz > 0:
        z = n - 1
        vz = -vz

    return (x, y, z), (vx, vy, vz)
