from unittest import TestCase
from pathfinder import RectangularObstacle, RectangularUnit, Point, find_path, line_crosses_obstacle


class TestFindingPath(TestCase):
    def test_no_obstacles(self):
        unit = RectangularUnit(Point(0, 0), 0.5, 0.5)
        destination = Point(3, 0)
        obstacles = []
        path = find_path(unit, destination, obstacles)
        self.assertEqual(path, [(3, 0)])

    def test_one_obstacle(self):
        unit = RectangularUnit(Point(0, 0), 0.5, 0.5)
        destination = Point(5, 0)
        obstacles = [RectangularObstacle(-3, 1, 2, 3)]
        path = find_path(unit, destination, obstacles)
        self.assertEquals(path, [Point(1.5, 1.5), Point(3.5, 1.5), Point(5, 0)])

    def test_no_path(self):
        unit = RectangularUnit(Point(0, 0), 0.5, 0.5)
        destination = Point(3, 0)
        obstacles = [
            RectangularObstacle(-1, 1, 1, 2),
            RectangularObstacle(-1, 1, 4, 5),
            RectangularObstacle(1, 2, 2, 4),
            RectangularObstacle(-2, -1, 2, 4)
        ]
        path = find_path(unit, destination, obstacles)
        self.assertEquals(path, None)

    def test_two_obstacles(self):
        unit = RectangularUnit(Point(0, 0), 0.5, 0.5)
        destination = Point(5, 0)
        obstacles = [
            RectangularObstacle(-3, 0.5, 1, 2),
            RectangularObstacle(-0.5, 3, 3, 4)
        ]
        path = find_path(unit, destination, obstacles)
        self.assertEquals(path, [Point(0.5, 1), Point(2.5, 1), Point(2.5, -1), Point(4.5, -1), Point(5, 0)])


class TestObstacleCrossing(TestCase):
    def test_through_the_middle(self):
        obstacle = RectangularObstacle(1, 3, 1, 3)
        p1 = Point(0, 0)
        p2 = Point(4, 4)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertTrue(result)

    def test_through_the_middle_x(self):
        obstacle = RectangularObstacle(1, 3, 1, 3)
        p1 = Point(0, 2)
        p2 = Point(4, 2)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertTrue(result)

    def test_through_the_middle_y(self):
        obstacle = RectangularObstacle(1, 3, 1, 3)
        p1 = Point(2, 0)
        p2 = Point(2, 4)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertTrue(result)

    def test_through_the_middle_reversed(self):
        obstacle = RectangularObstacle(1, 3, 1, 3)
        p1 = Point(4, 4)
        p2 = Point(0, 0)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertTrue(result)

    def test_through_the_middle_different_angle(self):
        obstacle = RectangularObstacle(1, 3, 1, 3)
        p1 = Point(0, 2.5)
        p2 = Point(3, 3.99)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertTrue(result)

    def test_no_collision(self):
        obstacle = RectangularObstacle(1, 3, 1, 3)
        p1 = Point(0, 0)
        p2 = Point(4, 0)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_parallel_edge_x(self):
        obstacle = RectangularObstacle(1, 3, 1, 3)
        p1 = Point(0, 1)
        p2 = Point(4, 1)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_parallel_edge_y(self):
        obstacle = RectangularObstacle(1, 3, 1, 3)
        p1 = Point(1, 0)
        p2 = Point(1, 4)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_tip(self):
        obstacle = RectangularObstacle(1, 3, 1, 3)
        p1 = Point(0, 2)
        p2 = Point(2, 4)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_starting_in_tip(self):
        obstacle = RectangularObstacle(1, 3, 1, 3)
        p1 = Point(1, 1)
        p2 = Point(0, 0)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_starting_in_tip_perpendicular(self):
        obstacle = RectangularObstacle(1, 3, 1, 3)
        p1 = Point(1, 1)
        p2 = Point(0, 1)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_touching_side_perpendicular(self):
        obstacle = RectangularObstacle(1, 3, 1, 3)
        p1 = Point(0, 2)
        p2 = Point(1, 2)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_not_crossing_but_pointing_perpendicular(self):
        obstacle = RectangularObstacle(1, 3, 1, 3)
        p1 = Point(-1, 2)
        p2 = Point(0, 2)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_not_crossing_but_pointing(self):
        obstacle = RectangularObstacle(1, 3, 1, 3)
        p1 = Point(-1, 2.5)
        p2 = Point(0, 2)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_pointing_away(self):
        obstacle = RectangularObstacle(1, 3, 1, 3)
        p1 = Point(4, 2)
        p2 = Point(5, 2.5)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)
