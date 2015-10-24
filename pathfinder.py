from collections import namedtuple, defaultdict
import numpy as np
import itertools
from functools import lru_cache


# TODO: eliminate duplicate points!
Obstacle = namedtuple('Obstacle', 'up down left right')
Point = namedtuple('Point', 'x y')
Adjacency = namedtuple('Adjacency', 'distance point')


class Agent:
    def __init__(self, position, size_x, size_y, velocity=1.0):
        self.position = position
        self.size_x = size_x
        self.size_y = size_y
        self.path = []
        self.velocity = velocity

    def is_moving(self):
        return bool(self.path)

    def calculate_new_path(self, destination, obstacles):
        obstacles = self.create_obstacles_in_configuration_space(obstacles)
        self.path = find_path(self.position, destination, obstacles)

    @lru_cache(maxsize=8)
    def create_obstacles_in_configuration_space(self, obstacles):
        obstacles_in_configuration_space = [
            Obstacle(
                obs.up - self.size_y, obs.down + self.size_y,
                obs.left - self.size_x, obs.right + self.size_x)
            for obs in obstacles]
        return tuple(obstacles_in_configuration_space)

    def move_along_path(self):
        next_point = self.path[0]
        d = np.subtract(next_point, self.position)
        d_len = np.linalg.norm(d)

        if d_len < self.velocity:
            self.path.pop(0)
        else:
            d = np.divide(d, d_len)
            d = np.multiply(d, self.velocity)

        self.position = Point(*np.add(self.position, d))


def find_path(current_position, destination, obstacles):
    points = create_list_of_all_points(obstacles)
    connections = build_connections_graph(points, obstacles)
    connections = add_to_connections(current_position, obstacles, connections)
    connections = add_to_connections(destination, obstacles, connections)
    path = find_path_using_graph(current_position, destination, connections)
    return path


def find_path_using_graph(start, goal, connections):
    closedset = set()
    openset = set()
    openset.add(start)
    came_from = {}

    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0
    f_score = defaultdict(lambda: float('inf'))
    f_score[start] = g_score[start] + heuristic_cost_estimate(start, goal)

    while openset:
        current = next(node for node in openset if f_score[node] == min(f_score[n] for n in openset))
        if current == goal:
            return reconstruct_path(came_from, goal)

        openset.remove(current)
        closedset.add(current)
        for adjacency in connections[current]:
            neighbour = adjacency.point
            if neighbour in closedset:
                continue

            tentative_g_score = g_score[current] + adjacency.distance

            if neighbour not in openset or tentative_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = g_score[neighbour] + heuristic_cost_estimate(neighbour, goal)
                if neighbour not in openset:
                    openset.add(neighbour)

    return None


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    total_path.pop(0)
    return total_path


def heuristic_cost_estimate(point, goal):
    return np.linalg.norm(np.subtract(point, goal))


@lru_cache(maxsize=8)
def create_list_of_all_points(obstacles):
    points = set()
    for obs in obstacles:
        points.update([Point(x, y) for x, y in itertools.product([obs.left, obs.right], [obs.up, obs.down])])
    return tuple(points)


@lru_cache(maxsize=8)
def build_connections_graph(points, obstacles):
    graph = {}
    for point in points:
        graph[point] = []

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p1 = points[i]
            p2 = points[j]

            crossed_obstacles = [obs for obs in obstacles if line_crosses_obstacle(p1, p2, obs)]
            if not crossed_obstacles:
                distance = np.linalg.norm(np.subtract(p1, p2))
                graph[p1].append(Adjacency(distance, p2))
                graph[p2].append(Adjacency(distance, p1))

    return graph


def add_to_connections(point, obstacles, graph):
    graph[point] = []

    p1 = point
    for p2 in graph.keys():
        crossed_obstacles = [obs for obs in obstacles if line_crosses_obstacle(p1, p2, obs)]
        if not crossed_obstacles:
            distance = np.linalg.norm(np.subtract(p1, p2))
            graph[p1].append(Adjacency(distance, p2))
            graph[p2].append(Adjacency(distance, p1))

    return graph


def line_crosses_obstacle(p1, p2, obstacle):
        if p1 == p2:
            return False

        e = Point(*p1)
        d = np.subtract(p2, p1)
        d_len = np.linalg.norm(d)
        d = np.divide(d, d_len)
        d = Point(*d)

        with np.errstate(divide='ignore', invalid='ignore'):
            ax = np.divide(1, d.x)
            ay = np.divide(1, d.y)

            if ax >= 0:
                txmin = np.multiply(ax, obstacle.left - e.x)
                txmax = np.multiply(ax, obstacle.right - e.x)
            else:
                txmin = np.multiply(ax, obstacle.right - e.x)
                txmax = np.multiply(ax, obstacle.left - e.x)

            if ay >= 0:
                tymin = np.multiply(ay, obstacle.up - e.y)
                tymax = np.multiply(ay, obstacle.down - e.y)
            else:
                tymin = np.multiply(ay, obstacle.down - e.y)
                tymax = np.multiply(ay, obstacle.up - e.y)

        return txmin < tymax and tymin < txmax and txmin < d_len and tymin < d_len and txmax > 0 and tymax > 0
