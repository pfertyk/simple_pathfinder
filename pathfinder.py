from collections import namedtuple, defaultdict
import numpy as np
import itertools
import functools

# TODO: better names for fields in Unit?
# TODO: eliminate duplicate points!
# TODO: empty path instead of None?
# TODO: return tuples or Points?
# TODO: test for destination inside obstacle
# TODO: test: Clicked:  119 440 Clicked:  744 56 Clicked:  67 120 Clicked:  107 152 Clicked:  114 148 Clicked:  120 304
# TODO: test: Clicked:  315 576 Clicked:  458 228 Clicked:  234 444
# TODO: serious optimalization (caching? better algorithm? other data structures?)
# TODO: tower defense game
RectangularObstacle = namedtuple('RectangularObstacle', 'up down left right')
RectangularUnit = namedtuple('RectangularUnit', 'position, size_x, size_y')
Point = namedtuple('Point', 'x y')
Adjacency = namedtuple('Adjacency', 'distance point')


def find_path(unit, destination, obstacles):
    new_obstacles = create_new_obstacles_for_size(unit.size_x, unit.size_y, obstacles)
    points = create_list_of_all_points(new_obstacles)
    connections = build_connections_graph(points, new_obstacles)
    connections = add_to_connections(unit.position, new_obstacles, connections)
    connections = add_to_connections(destination, new_obstacles, connections)
    path = find_path_using_graph(unit.position, destination, connections)
    return path


def my_cache_wrapper(func):
    print('init wrapper')
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if (func, args, str(kwargs)) in cache:
            print('found in cache')
            return cache[(func, args, str(kwargs))]
        else:
            tmp = func(*args, **kwargs)
            cache[(func, args, str(kwargs))] = tmp
            return tmp
    return wrapper


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


@my_cache_wrapper
def create_new_obstacles_for_size(size_x, size_y, obstacles):
    new_obstacles = [
        RectangularObstacle(
            obs.up - size_y, obs.down + size_y,
            obs.left - size_x, obs.right + size_x)
        for obs in obstacles]
    return tuple(new_obstacles)


@my_cache_wrapper
def create_list_of_all_points(obstacles):
    points = set()
    for obs in obstacles:
        points.update([Point(x, y) for x, y in itertools.product([obs.left, obs.right], [obs.up, obs.down])])
    return tuple(points)


@my_cache_wrapper
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

if __name__ == '__main__':
    print('Hello!')
    print(np.divide(1, 0))
    print(np.divide(-1.0, 0.0))
    print(np.divide(0.0, 0.0))
    p = Point(4, 3)
    l = np.linalg.norm(p)
    print(l)
    p /= l
    print(p)
    o = RectangularObstacle(1, 2, 3, 4)
    print([Point(x, y) for x, y in itertools.product([o.left, o.right], [o.up, o.down])])
    for elem in range(2, 1):
        print('Hello!' + elem)
    print(range(2, 1))
