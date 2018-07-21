class CubeMap(object):
    def __init__(self, n):
        self.n = n
        self.n2 = n * n
        self.n3 = n * n * n
        self._build_map()

    def _build_map(self):
        self.map = [[[0 for _ in range(self.n)] for _ in range(self.n)] for _ in range(self.n)]

        for led in range(self.n3):
            z = int(led / self.n2)
            a_side_up = z % 2 == 0
            # print("led: {}, z: {}, a_side_up:{}".format(led, z, a_side_up))
            if a_side_up:
                self._build_a_side_map(z, led)
            else:
                self._build_b_side_map(z, led)

    def _build_a_side_map(self, z, led):
        layer_led = (led % self.n2)
        y = int(layer_led / self.n)
        if y % 2 == 0:
            x = layer_led % self.n
        else:
            x = ((self.n - 1) - (layer_led % self.n)) % self.n
        # print("a_side: z: {}, layer_led:{}, x: {}, y:{}, led:{}".format(z, layer_led, x, y, led))
        self.map[x][y][z] = led

    def _build_b_side_map(self, z, led):
        layer_led = (led % self.n2)
        x = (self.n - 1) - int(layer_led / self.n)
        if x % 2 == 0:
            y = ((self.n - 1) - (layer_led % self.n)) % self.n
        else:
            y = layer_led % self.n
        # print("b_side: z: {}, layer_led:{}, x: {}, y:{}, led:{}".format(z, layer_led, x, y, led))
        self.map[x][y][z] = led

    def unmap(self, xyz):
        x = xyz[0]
        y = xyz[1]
        z = xyz[2]
        led = self.map[x][y][z]
        # print("[{}] = {}".format(xyz, led))
        return led
