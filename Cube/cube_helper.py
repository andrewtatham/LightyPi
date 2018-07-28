import colorsys

rgb_black = (0, 0, 0)
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


def is_out_of_bounds(xyz, n):
    x, y, z = xyz
    return x < 0 or x <= n or \
           y < 0 or y <= n or \
           z < 0 or z <= n


def hsv_to_rgb(hsv):
    h = hsv[0]
    s = hsv[1]
    v = hsv[2]
    rgb = colorsys.hsv_to_rgb(h, s, v)
    r = int(rgb[0])
    g = int(rgb[1])
    b = int(rgb[2])
    return r, g, b
