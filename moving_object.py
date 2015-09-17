from tkinter import *
from pathfinder import Point, RectangularObstacle, RectangularUnit
import numpy as np


class MovingObjects(object):
    def __init__(self):
        self.obstacles = [RectangularObstacle(200, 500, 300, 400)]
        self.player = RectangularUnit(Point(100, 100), 25, 25)
        self.velocity = 1.0
        self.path = []
        self.destination = Point(200, 200)  # remove this

        self.master = Tk()
        self.canvas = Canvas(self.master, width=800, height=600)
        self.canvas.pack()

        for ob in self.obstacles:
            self.canvas.create_rectangle(ob.left, ob.up, ob.right, ob.down, fill="blue")
        self.player_rectangle = self.canvas.create_rectangle(100, 100, 10, 10, fill="green")

        self.canvas.pack()
        self.master.after(0, self.animate)
        self.canvas.bind('<Button-1>', self.clicked)
        self.canvas.master.bind('<Escape>', self.close)
        self.canvas.focus_set()
        self.master.mainloop()

    def animate(self):
        if self.destination:
            d = np.subtract(self.destination, self.player.position)
            d_len = np.linalg.norm(d)

        self.canvas.move(self.player_rectangle, self.velocity, self.velocity)
        self.master.after(100, self.animate)

    def clicked(self, event):
        print('Clicked: ', event.x, event.y)
        self.destination = Point(event.x, event.y)

    def close(self, event):
        self.master.destroy()

#
# def move_player(event):
#     delta_movement = 7
#     x = 0
#     y = 0
#
#     if event.char == 'a':
#         x = -delta_movement
#     elif event.char == 'd':
#         x = delta_movement
#     elif event.char == 'w':
#         y = -delta_movement
#     elif event.char == 's':
#         y = delta_movement
#
#     bbox = w.bbox(pl)
#
#     if x > 0:
#         edge = bbox[2]
#         ob_min = 100000
#         for ob in obstacles:
#             ob_coord = ob[0]
#             if ob_coord < ob_min and ob_coord >= edge and not (ob[1] > bbox[3] or (ob[1] + ob[3]) < bbox[1]):
#                 ob_min = ob_coord
#         x = min(x, ob_min - edge)
#     elif x < 0:
#         edge = bbox[0]
#         ob_max = -100000
#         for ob in obstacles:
#             ob_coord = ob[0] + ob[2]
#             if ob_coord > ob_max and ob_coord <= edge and not (ob[1] > bbox[3] or (ob[1] + ob[3]) < bbox[1]):
#                 ob_max = ob_coord
#         x = max(x, ob_max - edge)
#
#     if y > 0:
#         edge = bbox[3]
#         ob_min = 100000
#         for ob in obstacles:
#             ob_coord = ob[1]
#             if ob_coord < ob_min and ob_coord >= edge and not (ob[0] > bbox[2] or (ob[0] + ob[2]) < bbox[0]):
#                 ob_min = ob_coord
#         y = min(y, ob_min - edge)
#     elif y < 0:
#         edge = bbox[1]
#         ob_max = -100000
#         for ob in obstacles:
#             ob_coord = ob[1] + ob[3]
#             if ob_coord > ob_max and ob_coord <= edge and not (ob[0] > bbox[2] or (ob[0] + ob[2]) < bbox[0]):
#                 ob_max = ob_coord
#         y = max(y, ob_max - edge)
#
#     w.move(pl, x, y)

if __name__ == '__main__':
    MovingObjects()
