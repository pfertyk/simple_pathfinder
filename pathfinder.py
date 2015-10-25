from collections import namedtuple, defaultdict
from functools import lru_cache
import numpy as np
import itertools

Obstacle = namedtuple('Obstacle', 'up down left right')
Point = namedtuple('Point', 'x y')
Adjacency = namedtuple('Adjacency', 'distance point')


class Agent:
    """
    Represents a rectangular Agent moving among rectangular obstacles.

    The position of the Agent is located in the center of his rectangle.
    The value of size_x represents the distance from Agent's position
    to both the left and right side of that rectangle. Similarly, the
    value of size_y represents the distance from Agent's position to
    both the upper and lower side of that rectangle. Therefore, the
    dimension of the Agent's rectangle is (2*size_x, 2*size_y).
    """
    def __init__(self, position, size_x, size_y, velocity=1.0):
        self.position = position
        self.size_x = size_x
        self.size_y = size_y
        self.path = []
        self.velocity = velocity

    def is_moving(self):
        """
        Checks if the Agent is moving (if he has a path to follow).
        """
        return bool(self.path)

    def calculate_new_path(self, destination, obstacles):
        """
        Calculates new path from Agent's current position to given destination and stores this path.
        """
        obstacles = self.create_obstacles_in_configuration_space(obstacles)
        self.path = find_path(self.position, destination, obstacles)

    @lru_cache(maxsize=8)
    def create_obstacles_in_configuration_space(self, obstacles):
        """
        Creates new 'inflated' obstacles.

        Each obstacle is transformed by increasing its size by the size
        of the Agent. That allows the Agent to be represented as a single
        point instead of a rectangle.
        """
        obstacles_in_configuration_space = [
            Obstacle(
                obs.up - self.size_y, obs.down + self.size_y,
                obs.left - self.size_x, obs.right + self.size_x)
            for obs in obstacles]
        return tuple(obstacles_in_configuration_space)

    def move_along_path(self):
        """
        Moves the Agent and updates his path.

        Takes the next point of current path. If that point is close enough
        (within one velocity distance), moves the agent to that point and
        removes the point from path. Otherwise moves the agent by one velocity
        distance toward that point.

        If the path is empty, the method doesn't do anything.
        """
        if not self.path:
            return
        next_point = self.path[0]
        next_point_delta = np.subtract(next_point, self.position)
        distance_to_next_point = np.linalg.norm(next_point_delta)

        if distance_to_next_point < self.velocity:
            self.position = self.path.pop(0)
        else:
            velocity_vector = np.multiply(next_point_delta, self.velocity / distance_to_next_point)
            new_position = np.add(self.position, velocity_vector)
            self.position = Point(*new_position)


def find_path(start, destination, obstacles):
    """
    Calculates the path between start and destination, avoiding the obstacles.

    Both the start and the destination are considered to be points
    (with no dimensions). Returned path is a list of points that need
    to be visited (in order) to reach from start to destination.
    The path does not contain the starting point, since that point
    is already visited. The path contains the destination as its
    last element.
    """
    visibility_graph = create_visibility_graph(start, destination, obstacles)
    path = find_path_using_visibility_graph(start, destination, visibility_graph)
    return path


def create_visibility_graph(start, destination, obstacles):
    """
    Creates a visibility graph.

    The graph is a dictionary. The key set contains all the vertices
    (corners) of all the obstacles as well as start and destination
    points. The value for each key is a list of adjacent points and
    distances to those points. Each entry on the list is in a form
    of a tuple containing a distance and a point. A point is
    considered adjacent to a given one if there is an unobstructed
    line between them (if the line does not intersect with any
    obstacle). If a list of adjacent points for p1 contains p2,
    then the list of adjacent points for p2 will contain p1. The
    list of adjacent points might be empty, if the point has no
    adjacent ones.
    """
    visibility_graph = create_visibility_graph_for_obstacles(obstacles)
    add_vertex_to_visibility_graph(start, obstacles, visibility_graph)
    add_vertex_to_visibility_graph(destination, obstacles, visibility_graph)
    return visibility_graph


def find_path_using_visibility_graph(start, destination, visibility_graph):
    """
    Finds path from start to destination using visibility graph and A* algorithm.
    """
    nodes_to_visit = set()
    nodes_to_visit.add(start)
    visited_nodes = set()
    came_from_graph = {}

    distance_from_start = defaultdict(lambda: float('inf'))
    distance_from_start[start] = 0
    estimated_distance = defaultdict(lambda: float('inf'))
    estimated_distance[start] = distance_estimate(start, destination)

    while nodes_to_visit:
        min_estimated_distance = min(estimated_distance[n] for n in nodes_to_visit)
        current_node = next(node for node in nodes_to_visit if estimated_distance[node] == min_estimated_distance)
        if current_node == destination:
            return reconstruct_path_to_point(destination, came_from_graph)
        nodes_to_visit.remove(current_node)
        visited_nodes.add(current_node)
        for adjacency in visibility_graph[current_node]:
            neighbour_node = adjacency.point
            if neighbour_node in visited_nodes:
                continue
            neighbour_distance = distance_from_start[current_node] + adjacency.distance
            if neighbour_node not in nodes_to_visit or neighbour_distance < distance_from_start[neighbour_node]:
                came_from_graph[neighbour_node] = current_node
                distance_from_start[neighbour_node] = neighbour_distance
                estimated_distance[neighbour_node] = neighbour_distance + distance_estimate(neighbour_node, destination)
                if neighbour_node not in nodes_to_visit:
                    nodes_to_visit.add(neighbour_node)
    return None


def reconstruct_path_to_point(point, came_from_graph):
    """
    Creates a path from start to destination.

    Uses the graph (dictionary) of preceding nodes (created by A* algorithm).
    The path does not contain a starting point.
    """
    path = []
    while point in came_from_graph:
        path.insert(0, point)
        point = came_from_graph[point]
    return path


@lru_cache(maxsize=128)
def distance_estimate(point, goal):
    """
    Returns Euclidean distance between given points.
    """
    return np.linalg.norm(np.subtract(point, goal))


@lru_cache(maxsize=8)
def get_all_vertices(obstacles):
    """
    Returns a set of all vertices (corners) of given obstacles.
    """
    vertices = set()
    for obs in obstacles:
        vertices.update([Point(x, y) for x, y in itertools.product([obs.left, obs.right], [obs.up, obs.down])])
    return vertices


@lru_cache(maxsize=8)
def create_visibility_graph_for_obstacles(obstacles):
    """
    Creates a visibility graph only for given obstacles (with no start and destination).

    This was extracted as a separate method to allow caching.
    Obstacles in this program are considered immutable: no new
    obstacles appear and the existing ones do not move. Therefore,
    there is no reason to calculate the visibility graph for
    obstacles more than once. However, the start and destination
    change very often, so visibility for them is calculated using another method.
    """
    vertices = get_all_vertices(obstacles)
    visited_vertices = set()
    graph = {v: [] for v in vertices}
    for p1 in vertices:
        visited_vertices.add(p1)
        for p2 in vertices - visited_vertices:
            check_connection_between_points(graph, obstacles, p1, p2)
    return graph


def check_connection_between_points(graph, obstacles, point1, point2):
    """
    Checks if there is an unobstructed line between point1 and point2. If so, adds the adjacency to graph.
    """
    crossed_obstacles = [obs for obs in obstacles if line_crosses_obstacle(point1, point2, obs)]
    if not crossed_obstacles:
        distance = np.linalg.norm(np.subtract(point1, point2))
        graph[point1].append(Adjacency(distance, point2))
        graph[point2].append(Adjacency(distance, point1))


def add_vertex_to_visibility_graph(point, obstacles, graph):
    """
    Adds one vertex to visibility graph and calculates adjacent points for it.
    """
    points = set(graph.keys())
    graph[point] = []
    for existing_point in points:
        check_connection_between_points(graph, obstacles, point, existing_point)


def line_crosses_obstacle(point1, point2, obstacle, threshold=1e-10):
    """
    Checks if a line between 2 points crosses an obstacle.

    Line that overlaps the obstacle's side or shares only
    one point with the obstacle (e.g. one point is outside
    the obstacle and the other is in its vertex) is not
    considered to cross that obstacle.
    """
    if point1 == point2:
        return False
    e = Point(*point1)
    d = np.subtract(point2, point1)
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
