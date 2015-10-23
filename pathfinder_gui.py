from tkinter import *
from pathfinder import Point, RectangularObstacle, RectangularUnit, find_path
import numpy as np
import time


class PathfinderGUI(object):
    def __init__(self):
        self.obstacles = (
            RectangularObstacle(70, 90, 70, 700),
            RectangularObstacle(90, 510, 70, 90),
            RectangularObstacle(510, 530, 70, 400),
            RectangularObstacle(90, 300, 680, 700),
            RectangularObstacle(370, 540, 680, 700),
            RectangularObstacle(150, 360, 160, 180),
            RectangularObstacle(150, 170, 180, 380),
            RectangularObstacle(150, 290, 380, 400),
            RectangularObstacle(290, 310, 290, 550),
            RectangularObstacle(310, 500, 500, 520),
        )

        self.agent = RectangularUnit(Point(30, 30), 25, 25)
        self.velocity = 8.0
        self.path = []
        self.fps = 25

        self.master = Tk()
        self.master.wm_title('Left click to point destination, Esc to exit')
        self.master.after(0, self.animate)

        self.canvas = Canvas(self.master, width=800, height=600)

        for ob in self.obstacles:
            self.canvas.create_rectangle(ob.left, ob.up, ob.right, ob.down, fill="blue")

        self.player_rectangle = self.canvas.create_rectangle(
            self.agent.position.x - self.agent.size_x,
            self.agent.position.y - self.agent.size_y,
            self.agent.position.x + self.agent.size_x,
            self.agent.position.y + self.agent.size_y, fill="green")

        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.clicked)
        self.canvas.master.bind('<Escape>', self.close_window)
        self.canvas.focus_set()

        self.master.mainloop()

    def animate(self):
        if self.path:
            next_point = self.path[0]
            d = np.subtract(next_point, self.agent.position)
            d_len = np.linalg.norm(d)

            if d_len < self.velocity:
                self.path.pop(0)
            else:
                d = np.divide(d, d_len)
                d = np.multiply(d, self.velocity)

            new_position = np.add(self.agent.position, d)
            new_position = Point(*new_position)
            int_x = int(new_position.x) - int(self.agent.position.x)
            int_y = int(new_position.y) - int(self.agent.position.y)
            self.agent = RectangularUnit(new_position, self.agent.size_x, self.agent.size_y)
            self.canvas.move(self.player_rectangle, int_x, int_y)
        self.master.after(int(1000 / self.fps), self.animate)

    def clicked(self, event):
        print('Clicked: ', event.x, event.y)
        start = time.time()
        self.path = find_path(self.agent, Point(event.x, event.y), self.obstacles)
        end = time.time()
        print(end-start)

    def close_window(self, event):
        self.master.destroy()

if __name__ == '__main__':
    PathfinderGUI()
