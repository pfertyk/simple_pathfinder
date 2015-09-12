from collections import namedtuple

__author__ = 'pawel'

RectangularObstacle = namedtuple('RectangularObstacle', 'up down left right')
# TODO: better names for fields in Unit?
RectangularUnit = namedtuple('RectangularUnit', 'middle_x, middle_y, size_x, size_y')

class Pathfinder:
    @staticmethod
    def find_path(unit, destination, obstacles):
        return [destination]

if __name__ == '__main__':
    print('Hello!')