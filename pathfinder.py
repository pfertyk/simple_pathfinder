from collections import namedtuple
import numpy as np
import itertools
from queue import Queue

# TODO: better names for fields in Unit?
# TODO: svg visualization of found paths
# TODO: turn off warning 'divide by zero'
# TODO: eliminate duplicate points!
# TODO: empty path instead of None?
# TODO: return tuples or Points?
RectangularObstacle = namedtuple('RectangularObstacle', 'up down left right')
RectangularUnit = namedtuple('RectangularUnit', 'position, size_x, size_y')
Point = namedtuple('Point', 'x y')


def find_path(unit, destination, obstacles):
    new_obstacles = create_new_obstacles_for_unit(unit, obstacles)
    points = create_list_of_all_points(unit.position, destination, new_obstacles)
    connections = build_connections_graph(points, new_obstacles)
    path = find_path_using_graph(unit.position, destination, connections)
    return path


def find_path_using_graph(position, destination, connections):
    distances = {destination: 0.0}

    points_to_visit = Queue()
    points_to_visit.put(destination)

    while not points_to_visit.empty():
        current_point = points_to_visit.get()
        current_distance = distances[current_point]
        next_points = connections[current_point]
        for next_point in next_points:
            new_distance = current_distance + np.linalg.norm(np.subtract(current_point, next_point))
            if next_point not in distances.keys() or distances[next_point] > new_distance:
                distances[next_point] = new_distance
                points_to_visit.put(next_point)

    if position in distances.keys():
        path = []
        current_point = position
        current_distance = distances[current_point]

        while current_distance > 0:
            connected_points = connections[current_point]
            min_distance = min(distances[point] for point in connected_points)
            current_point = next(point for point in connected_points if distances[point] == min_distance)
            path.append(current_point)
            current_distance = distances[current_point]
    else:
        path = None

    return path


def create_new_obstacles_for_unit(unit, obstacles):
    new_obstacles = [
        RectangularObstacle(
            obs.up - unit.size_y, obs.down + unit.size_y,
            obs.left - unit.size_x, obs.right + unit.size_x)
        for obs in obstacles]
    return new_obstacles


def create_list_of_all_points(position, destination, obstacles):
    points = {position, destination}
    for obs in obstacles:
        points.update([Point(x, y) for x, y in itertools.product([obs.left, obs.right], [obs.up, obs.down])])
    return list(points)


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
                graph[p1].append(p2)
                graph[p2].append(p1)

    return graph


def line_crosses_obstacle(p1, p2, obstacle):
        if p1 == p2:
            return False

        e = Point(*p1)
        d = np.subtract(p2, p1)
        d_len = np.linalg.norm(d)
        d = np.divide(d, d_len)
        d = Point(*d)

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
