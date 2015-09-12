from unittest import TestCase
from pathfinder import Pathfinder, RectangularObstacle, RectangularUnit

__author__ = 'pawel'


class TestPathfinder(TestCase):
    def test_no_obstacles(self):
        unit = RectangularUnit(0, 0, 0.5, 0.5)
        destination = (3, 0)
        obstacles = []
        path = Pathfinder().find_path(unit, destination, obstacles)
        self.assertEqual(path, [(3, 0)])

    def test_one_obstacle(self):
        unit = RectangularUnit(0, 0, 0.5, 0.5)
        destination = (5, 0)
        obstacles = [RectangularObstacle(1, -3, 2, 3)]
        path = Pathfinder().find_path(unit, destination, obstacles)
        self.assertEquals(path, [(1.5, 1.5), (3.5, 1.5), (5, 0)])

    def test_no_path(self):
        unit = RectangularUnit(0, 0, 0.5, 0.5)
        destination = (3, 0)
        obstacles = [
            RectangularObstacle(1, -1, 1, 2),
            RectangularObstacle(1, -1, 4, 5),
            RectangularObstacle(2, 1, 2, 4),
            RectangularObstacle(-1, -2, 2, 4)
        ]
        path = Pathfinder().find_path(unit, destination, obstacles)
        self.assertEquals(path, None)
