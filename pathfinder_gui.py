from pathfinder import Point, Obstacle, Agent
import tkinter
import time


class PathfinderGUI:
    """
    Simple GUI for pathfinder module.

    Displays one Agent (green) and 10 obstacles (blue). New
    destination can be selected by left clicking on canvas.
    Pressing Esc closes the program.
    """
    def __init__(self):
        self.obstacles = (
            Obstacle(70, 90, 70, 700),
            Obstacle(90, 510, 70, 90),
            Obstacle(510, 530, 70, 400),
            Obstacle(90, 300, 680, 700),
            Obstacle(370, 540, 680, 700),
            Obstacle(150, 360, 160, 180),
            Obstacle(150, 170, 180, 380),
            Obstacle(150, 290, 380, 400),
            Obstacle(290, 310, 290, 550),
            Obstacle(310, 500, 500, 520),
        )
        self.agent = Agent(Point(30, 30), 25, 25, velocity=8)
        self.fps = 25
        self.is_animating = False
        self.pre_calculate_paths()

        self.master = tkinter.Tk()
        self.master.wm_title('Left click to select destination, Esc to exit')
        self.master.bind('<Escape>', self.close_window)

        self.canvas = tkinter.Canvas(self.master, width=800, height=600)
        self.init_canvas()

        self.master.mainloop()

    def init_canvas(self):
        """
        Draws all objects (Agent and obstacles) on canvas and binds click event.
        """
        self.canvas.create_rectangle(0, 0, 1, 1, fill='green', tags='agent')
        for ob in self.obstacles:
            self.canvas.create_rectangle(ob.left, ob.up, ob.right, ob.down, fill='blue')

        self.redraw_agent()
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.calculate_new_path)
        self.canvas.focus_set()

    def redraw_agent(self):
        """
        Updates position of the Agent on canvas.
        """
        self.canvas.coords(
            'agent',
            self.agent.position.x - self.agent.size_x,
            self.agent.position.y - self.agent.size_y,
            self.agent.position.x + self.agent.size_x,
            self.agent.position.y + self.agent.size_y)

    def animate_agent(self):
        """
        Moves the Agent along his path and redraws him.

        If the Agent has not reached his destination, this function will call
        itself again after the specified interval (depends on fps settings).
        """
        self.is_animating = True

        if self.agent.is_moving():
            self.agent.move_along_path()
            self.redraw_agent()
            self.master.after(int(1000 / self.fps), self.animate_agent)
        else:
            self.is_animating = False

    def calculate_new_path(self, event):
        """
        Calculates new path for the Agent.

        Uses position of clicked point as a new destination and tells
        the Agent to calculate new path. If the Agent is currently not
        moving, this function will start the animation.
        """
        print('Selected destination: ', event.x, event.y)
        destination = Point(event.x, event.y)

        time1 = time.time()
        self.agent.calculate_new_path(destination, self.obstacles)
        time2 = time.time()
        print('Calculating path took %f s' % (time2 - time1))

        if not self.is_animating:
            self.animate_agent()

    def close_window(self, event):
        self.master.destroy()

    def pre_calculate_paths(self):
        """
        Calculates path using Agent's current position as destination.

        Does not actually move the Agent, but causes some values
        to be stored in cache, speeding up future calculations.
        """
        self.agent.calculate_new_path(self.agent.position, self.obstacles)

if __name__ == '__main__':
    PathfinderGUI()
