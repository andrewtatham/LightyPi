import unittest

from cube_map import CubeMap


class CubeMapTests(unittest.TestCase):
    def test_unmap(self):
        map = CubeMap(5)
        cases = [
            # Bottom layer (A side up) first row
            (0, (0, 0, 0)),
            (1, (1, 0, 0)),
            (2, (2, 0, 0)),
            (3, (3, 0, 0)),
            (4, (4, 0, 0)),
            # Bottom layer (A side up) second row
            (5, (4, 1, 0)),
            (6, (3, 1, 0)),
            (7, (2, 1, 0)),
            (8, (1, 1, 0)),
            (9, (0, 1, 0)),
            # Second Layer: 25+ and z = 1
            # Second layer (B side up) Last col
            (25 + 0, (4, 4, 1)),
            (25 + 1, (4, 3, 1)),
            (25 + 2, (4, 2, 1)),
            (25 + 3, (4, 1, 1)),
            (25 + 4, (4, 0, 1)),
            # Second layer (B side up) fourth col
            (25 + 5, (3, 0, 1)),
            (25 + 6, (3, 1, 1)),
            (25 + 7, (3, 2, 1)),
            (25 + 8, (3, 3, 1)),
            (25 + 9, (3, 4, 1)),

        ]
        for case in cases:
            with self.subTest(case):
                xyz = case[1]
                actual_led = map.unmap(xyz)
                expected_led = case[0]
                self.assertEqual(actual_led, expected_led)
