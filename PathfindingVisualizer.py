import pygame
from Widgets import *
from Algorithms import BFS
import time

clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 20)
BLUE = (51, 173, 255)
WIDTH = 800


EMPTY = 0 # Empty cell
WALL = 1 # wall/obstacle in the board
POINT = 2 # Endpoint in the board


class App:
    def __init__(self):
        # Initializing pygame and screen
        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode((1200, WIDTH))
        self.display.fill(WHITE)

        self.rows = 10

        # Board object used to drawing on screen
        self.on_screen_board = Board(self.display, WIDTH, WIDTH, self.rows)
        self.menu = Menu(self.display, self.reset_board, self.start)

        self.env = [([EMPTY] * 10) for i in range(10)] # actual board, at the start 5x5

        """ First drawing two points that the algorithm will connect
        only then when finished, procced to drawing walls.
        if a point is deleted -> back to True """
        self.drawing_endpoints = True
        self.total_endpoints = 0
        self.down = False # mouse down in general
        self.erase = True # list time the btn was clicked, it was the erase func
        self.started = False # True if the pathfinding is happenning
        self.needs_restart = False

    def run(self):
        """ Main loop of the app """
        while True:
            # Limit app to 60 FPS
            clock.tick(60)
            if self.started:
                self.while_running()

            for event in pygame.event.get():
                self.menu.handle_event(event)
                if event.type == pygame.QUIT:
                    return
                if not self.started and not self.needs_restart:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.mouse_down(event)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.down = False
                    elif event.type == pygame.MOUSEMOTION:
                        self.moving_mouse()

            self.on_screen_board.update() # Every tick update animation
            pygame.display.update() # Update screen

    def while_running(self):
        # called every frame (maybe twice per frame) to update
        # the pathfinding generator and screen
        # and check if already found path
        row, col = next(self.search)
        if isinstance(row, bool):
            if row == True:
                self.on_screen_board.add_square(col[0], col[1], BLACK)
            else:
                self.started = False
                self.needs_restart = True
        else:
            self.on_screen_board.add_square(row, col, BLUE)


    def mouse_down(self, event):
        """ Mouse was clicked """
        row, col = pos_to_row(pygame.mouse.get_pos(), self.rows)
        self.erase = True if event.button == 3 else False
        mouse_pos = pygame.mouse.get_pos()

        if self.drawing_endpoints:
            if not self.erase and self.on_screen_board.clicked(mouse_pos):
                self.add_to_board(row, col, POINT)

        # Else trying removing point if erase if on
        elif self.erase and self.on_screen_board.clicked(mouse_pos):
            self.remove_from_board(row, col)

        # Check if click was on board
        if self.on_screen_board.clicked(mouse_pos):
            self.down = True
            self.moving_mouse() # First when clicking draw square

    def moving_mouse(self):
        """ Mouse was moved over app """
        # check if mouse is on board, if yes and mouse is down, add WALL
        if self.down and self.on_screen_board.clicked(pygame.mouse.get_pos()):
            row, col = pos_to_row(pygame.mouse.get_pos(), self.rows)
            if self.erase:
                self.remove_from_board(row, col)
            else:
                if not self.drawing_endpoints:
                    self.add_to_board(row, col, WALL)

    def add_to_board(self, row, col, Type):
        """ mouse click needs to add to board """
        if Type == WALL:
            if self.env[row][col] == POINT:
                return # Don't allow drawing over points
            self.env[row][col] = WALL
            self.on_screen_board.add_square(row, col, GREEN)
        else:
            self.on_screen_board.add_square(row, col, BLACK)
            self.env[row][col] = POINT
            self.total_endpoints += 1
            if self.total_endpoints >= 2:
                self.drawing_endpoints = False

    def remove_from_board(self, row, col):
        """ mouse click needs to remove from board """
        if self.env[row][col] == WALL:
            self.env[row][col] = EMPTY
            self.on_screen_board.delete_square(row, col, GREEN)
        elif self.env[row][col] == POINT:
            self.env[row][col] = EMPTY
            self.total_endpoints -= 1
            self.drawing_endpoints = True
            self.on_screen_board.delete_square(row, col, BLACK)

    def reset_board(self, size):
        self.started = False
        self.needs_restart = False
        self.total_endpoints = 0
        self.drawing_endpoints = True
        self.rows = [8, 10, 16, 20, 40, 50][size]
        self.env = [([0] * self.rows) for i in range(self.rows)]
        self.on_screen_board = Board(self.display, WIDTH, WIDTH, self.rows)

    def start(self):
        if self.needs_restart or self.started:
            return
        self.search = BFS(self.env)
        self.started = True


def pos_to_row(pos, rows):
    size = WIDTH / rows
    column = pos[0] // size
    row = pos[1] // size
    return ((int(row), int(column)))


def __main__():
    app = App()
    app.run()

if __name__ == "__main__":
    __main__()
