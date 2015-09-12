from unittest import TestCase
from pathfinder import Pathfinder

__author__ = 'pawel'


class TestPathfinder(TestCase):
    def test_no_obstacles(self):
        start = (0, 0)
        destination = (0, 3)
        obstacles = []

        path = Pathfinder().findPath(start, destination, obstacles)

        self.assertEqual(path, [(0,3)])


