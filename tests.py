from unittest import TestCase
from pathfinder import Obstacle, Point, find_path, line_crosses_obstacle, Agent


class FindingPathTests(TestCase):
    def test_no_obstacles(self):
        position = Point(0, 0)
        destination = Point(3, 0)
        obstacles = ()
        path = find_path(position, destination, obstacles)
        self.assertEqual(path, [(3, 0)])

    def test_one_obstacle(self):
        position = Point(0, 0)
        destination = Point(5, 0)
        obstacles = tuple() + (Obstacle(-3, 1, 2, 3), )
        path = find_path(position, destination, obstacles)
        self.assertEquals(path, [Point(2, 1), Point(3, 1), Point(5, 0)])

    def test_no_path(self):
        position = Point(0, 0)
        destination = Point(3, 0)
        obstacles = (
            Obstacle(-2, 2, 1, 2),
            Obstacle(-2, 2, 4, 5),
            Obstacle(1, 2, 1, 5),
            Obstacle(-2, -1, 1, 5)
        )
        path = find_path(position, destination, obstacles)
        self.assertEquals(path, None)

    def test_two_obstacles(self):
        position = Point(0, 0)
        destination = Point(5, 0)
        obstacles = (
            Obstacle(-3, 0.5, 1, 2),
            Obstacle(-0.5, 3, 3, 4)
        )
        path = find_path(position, destination, obstacles)
        self.assertEquals(path, [Point(1, 0.5), Point(2, 0.5), Point(3, -0.5), Point(4, -0.5), Point(5, 0)])

    def test_shortest_path(self):
        position = Point(750, 290)
        destination = Point(607, 324)
        obstacles = (
            Obstacle(65, 325, 655, 725),
            Obstacle(265, 335, 265, 575)
        )
        path = find_path(position, destination, obstacles)
        self.assertEquals(path, [Point(725, 325), Point(655, 325), Point(607, 324)])

    def test_destination_inside_obstacle(self):
        position = Point(4, 4)
        destination = Point(0, 0)
        obstacles = tuple() + (Obstacle(-2, 2, -2, 2), )
        path = find_path(position, destination, obstacles)
        self.assertEquals(path, None)


class ObstacleCrossingTests(TestCase):
    def test_through_the_middle(self):
        obstacle = Obstacle(1, 3, 1, 3)
        p1 = Point(0, 0)
        p2 = Point(4, 4)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertTrue(result)

    def test_through_the_middle_x_aligned(self):
        obstacle = Obstacle(1, 3, 1, 3)
        p1 = Point(0, 2)
        p2 = Point(4, 2)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertTrue(result)

    def test_through_the_middle_y_aligned(self):
        obstacle = Obstacle(1, 3, 1, 3)
        p1 = Point(2, 0)
        p2 = Point(2, 4)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertTrue(result)

    def test_through_the_middle_reversed(self):
        obstacle = Obstacle(1, 3, 1, 3)
        p1 = Point(4, 4)
        p2 = Point(0, 0)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertTrue(result)

    def test_through_the_middle_different_angle(self):
        obstacle = Obstacle(1, 3, 1, 3)
        p1 = Point(0, 2.5)
        p2 = Point(3, 3.99)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertTrue(result)

    def test_no_collision(self):
        obstacle = Obstacle(1, 3, 1, 3)
        p1 = Point(0, 0)
        p2 = Point(4, 0)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_parallel_edge_x(self):
        obstacle = Obstacle(1, 3, 1, 3)
        p1 = Point(0, 1)
        p2 = Point(4, 1)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_parallel_edge_y(self):
        obstacle = Obstacle(1, 3, 1, 3)
        p1 = Point(1, 0)
        p2 = Point(1, 4)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_tip(self):
        obstacle = Obstacle(1, 3, 1, 3)
        p1 = Point(0, 2)
        p2 = Point(2, 4)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_starting_in_tip(self):
        obstacle = Obstacle(1, 3, 1, 3)
        p1 = Point(1, 1)
        p2 = Point(0, 0)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_starting_in_tip_perpendicular(self):
        obstacle = Obstacle(1, 3, 1, 3)
        p1 = Point(1, 1)
        p2 = Point(0, 1)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_touching_side_perpendicular(self):
        obstacle = Obstacle(1, 3, 1, 3)
        p1 = Point(0, 2)
        p2 = Point(1, 2)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_not_crossing_but_pointing_perpendicular(self):
        obstacle = Obstacle(1, 3, 1, 3)
        p1 = Point(-1, 2)
        p2 = Point(0, 2)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_not_crossing_but_pointing(self):
        obstacle = Obstacle(1, 3, 1, 3)
        p1 = Point(-1, 2.5)
        p2 = Point(0, 2)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_pointing_away(self):
        obstacle = Obstacle(1, 3, 1, 3)
        p1 = Point(4, 2)
        p2 = Point(5, 2.5)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertFalse(result)

    def test_one_point_inside(self):
        obstacle = Obstacle(1, 3, 1, 3)
        p1 = Point(0, 0)
        p2 = Point(2, 2)

        result = line_crosses_obstacle(p1, p2, obstacle)
        self.assertTrue(result)


class AgentMovementTests(TestCase):
    def test_destination_too_far(self):
        agent = Agent(Point(0, 0), 1, 1, 1)
        agent.path = [Point(10, 0)]

        agent.move_along_path()

        self.assertEqual(agent.path, [Point(10, 0)])
        self.assertEqual(agent.position, Point(1, 0))

    def test_destination_in_range(self):
        agent = Agent(Point(0, 0), 1, 1, 20)
        agent.path = [Point(10, 0)]

        agent.move_along_path()

        self.assertEqual(agent.path, [])
        self.assertEqual(agent.position, Point(10, 0))
