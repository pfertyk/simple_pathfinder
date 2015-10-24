from tkinter import *
from pathfinder import Point, RectangularObstacle, RectangularUnit, find_path, move_point_along_the_path
import time


class PathfinderGUI(object):
    def __init__(self):
        self.obstacles = create_sample_obstacles()
        self.agent = RectangularUnit(Point(30, 30), 25, 25)
        self.velocity = 8.0
        self.path = []
        self.fps = 25
        self.is_drawing = False

        self.master = Tk()
        self.master.wm_title('Left click to select destination, Esc to exit')
        self.master.bind('<Escape>', self.close_window)

        self.canvas = Canvas(self.master, width=800, height=600)
        self.player_rectangle = self.canvas.create_rectangle(0, 0, 1, 1, fill='green', tags='agent')
        self.init_canvas()

        self.master.mainloop()

    def init_canvas(self):
        for ob in self.obstacles:
            self.canvas.create_rectangle(ob.left, ob.up, ob.right, ob.down, fill='blue')
        self.redraw_agent()
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.calculate_new_path)
        self.canvas.focus_set()

    def redraw_agent(self):
        self.canvas.coords(
            'agent',
            self.agent.position.x - self.agent.size_x,
            self.agent.position.y - self.agent.size_y,
            self.agent.position.x + self.agent.size_x,
            self.agent.position.y + self.agent.size_y)

    def move_agent_along_path(self):
        self.is_drawing = True

        if self.path:
            new_position, new_path = move_point_along_the_path(self.agent.position, self.path, self.velocity)
            self.path = new_path
            self.agent = RectangularUnit(new_position, self.agent.size_x, self.agent.size_y)
            self.redraw_agent()

        if self.path:
            self.master.after(int(1000 / self.fps), self.move_agent_along_path)
        else:
            self.is_drawing = False

    def calculate_new_path(self, event):
        print('Selected destination: ', event.x, event.y)
        destination = Point(event.x, event.y)

        time1 = time.time()
        self.path = find_path(self.agent, destination, self.obstacles)
        time2 = time.time()
        print('Calculating path took %f s' % (time2 - time1))

        if not self.is_drawing:
            self.move_agent_along_path()

    def close_window(self, event):
        self.master.destroy()


def create_sample_obstacles():
    return (
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


if __name__ == '__main__':
    PathfinderGUI()
