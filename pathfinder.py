from collections import namedtuple, defaultdict
from functools import lru_cache
import numpy as np
import itertools

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
        next_point_delta = np.subtract(next_point, self.position)
        distance_to_next_point = np.linalg.norm(next_point_delta)

        if distance_to_next_point < self.velocity:
            self.position = self.path.pop(0)
        else:
            velocity_vector = np.multiply(next_point_delta, self.velocity / distance_to_next_point)
            new_position = np.add(self.position, velocity_vector)
            self.position = Point(*new_position)


def find_path(current_position, destination, obstacles):
    visibility_graph = create_visibility_graph(current_position, destination, obstacles)
    path = find_path_using_visibility_graph(current_position, destination, visibility_graph)
    return path


def create_visibility_graph(current_position, destination, obstacles):
    visibility_graph = create_visibility_graph_for_obstacles(obstacles)
    add_vertex_to_visibility_graph(current_position, obstacles, visibility_graph)
    add_vertex_to_visibility_graph(destination, obstacles, visibility_graph)
    return visibility_graph


def find_path_using_visibility_graph(start, destination, visibility_graph):
    nodes_to_visit = set()
    nodes_to_visit.add(start)
    visited_nodes = set()
    came_from_graph = {}

    distance_from_start = defaultdict(lambda: float('inf'))
    distance_from_start[start] = 0
    estimated_distance = defaultdict(lambda: float('inf'))
    estimated_distance[start] = distance_estimate(start, destination)

    while nodes_to_visit:
        current_node = next(node for node in nodes_to_visit if estimated_distance[node] == min(estimated_distance[n] for n in nodes_to_visit))
        if current_node == destination:
            return reconstruct_path_to_point(destination, came_from_graph)
        nodes_to_visit.remove(current_node)
        visited_nodes.add(current_node)
        for adjacency in visibility_graph[current_node]:
            neighbour_node = adjacency.point
            if neighbour_node in visited_nodes:
                continue
            neighbour_node_g_score = distance_from_start[current_node] + adjacency.distance
            if neighbour_node not in nodes_to_visit or neighbour_node_g_score < distance_from_start[neighbour_node]:
                came_from_graph[neighbour_node] = current_node
                distance_from_start[neighbour_node] = neighbour_node_g_score
                estimated_distance[neighbour_node] = distance_from_start[neighbour_node] + distance_estimate(neighbour_node, destination)
                if neighbour_node not in nodes_to_visit:
                    nodes_to_visit.add(neighbour_node)
    return None


def reconstruct_path_to_point(point, came_from_graph):
    path = []
    while point in came_from_graph:
        path.insert(0, point)
        point = came_from_graph[point]
    return path


@lru_cache(maxsize=128)
def distance_estimate(point, goal):
    return np.linalg.norm(np.subtract(point, goal))


@lru_cache(maxsize=8)
def get_all_vertices(obstacles):
    vertices = set()
    for obs in obstacles:
        vertices.update([Point(x, y) for x, y in itertools.product([obs.left, obs.right], [obs.up, obs.down])])
    return vertices


@lru_cache(maxsize=8)
def create_visibility_graph_for_obstacles(obstacles):
    vertices = get_all_vertices(obstacles)
    visited_vertices = set()
    graph = {v: [] for v in vertices}
    for p1 in vertices:
        visited_vertices.add(p1)
        for p2 in vertices - visited_vertices:
            check_connection_between_points(graph, obstacles, p1, p2)
    return graph


def check_connection_between_points(graph, obstacles, point1, point2):
    crossed_obstacles = [obs for obs in obstacles if line_crosses_obstacle(point1, point2, obs)]
    if not crossed_obstacles:
        distance = np.linalg.norm(np.subtract(point1, point2))
        graph[point1].append(Adjacency(distance, point2))
        graph[point2].append(Adjacency(distance, point1))


def add_vertex_to_visibility_graph(point, obstacles, graph):
    points = set(graph.keys())
    graph[point] = []
    for existing_point in points:
        check_connection_between_points(graph, obstacles, point, existing_point)


def line_crosses_obstacle(p1, p2, obstacle, threshold=1e-10):
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

        intervals_intersect = txmin < tymax - threshold and tymin < txmax - threshold
        intervals_are_valid = txmin < d_len and tymin < d_len and txmax > 0 and tymax > 0

        return intervals_intersect and intervals_are_valid
