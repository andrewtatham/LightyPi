import colorsys
import random

rgb_black = (0, 0, 0)


def get_random_colour():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


bys = {
    "x": lambda ijk: (ijk[0], ijk[1], ijk[2]),
    "y": lambda ijk: (ijk[2], ijk[0], ijk[1]),
    "z": lambda ijk: (ijk[1], ijk[2], ijk[0]),
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
    return random.randint(-1, +1), random.randint(-1, +1), random.randint(-1, +1)


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

    if x <= 0:
        x = 0
        vx = -vx
    if x >= n - 1:
        x = n - 1
        vx = -vx

    if y <= 0:
        y = 0
        vy = -vy
    if y >= n - 1:
        y = n - 1
        vy = -vy

    if z <= 0:
        z = 0
        vz = -vz
    if z >= n - 1:
        z = n - 1
        vz = -vz

    return (x, y, z), (vx, vy, vz)
