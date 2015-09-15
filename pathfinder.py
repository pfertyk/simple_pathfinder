from collections import namedtuple
import numpy as np

# TODO: better names for fields in Unit?
# TODO: svg visualization of found paths
# TODO: turn off warning 'divide by zero'
RectangularObstacle = namedtuple('RectangularObstacle', 'up down left right')
RectangularUnit = namedtuple('RectangularUnit', 'middle_x, middle_y, size_x, size_y')
Point = namedtuple('Point', 'x y')


class Pathfinder:
    @staticmethod
    def find_path(unit, destination, obstacles):
        new_obstacles = [
            RectangularObstacle(o.up - unit.size_y, o.down + unit.size_y, o.left - unit.size_x, o.right + unit.size_x)
            for o in obstacles]
        # build graph
        # find path
        return [destination]

    @staticmethod
    def line_crosses_obstacle(p1, p2, obstacle):
        if p1 == p2:
            return False

        e = p1
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

        # return not (txmin >= tymax or tymin >= txmax)
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
