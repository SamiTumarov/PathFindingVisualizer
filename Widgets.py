from pygame import Rect
from pygame.draw import rect
from pygame.font import SysFont
from Squares import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DEFAULT_COLOR = (107, 142, 35)
SELECTED_COLOR = (102, 205, 170)


class Button:
    def __init__(self, width, height, color, x, y, text=None):
        """ Represents button, provides functions such as drawing it on screen,
            checking if it was clicked (Providing the mouse pos),
            and the ability to change it's appearance """
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, display):
        rect(display, self.color, self.rect)
        if self.text:
            my_font = SysFont('Comic Sans MS', 30)
            text = my_font.render(self.text, False, (0, 0, 0))
            display.blit(text, (self.x + 10, self.y))

    def change_color(self, display, color):
        self.color = color
        self.draw(display)

    def clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class Board:
    def __init__(self, display, width, height, num_rows):
        """ Represents the board on screen, provides functions
        such as drawing the board, adding and deleting squares
        and updating their animations """
        self.width = width
        self.height = height
        self.size = self.width / num_rows
        self.num_rows = num_rows
        self.squares = []
        self.display = display

        self.draw_board()

    def draw_board(self):
        rect(self.display, WHITE, (0, 0, self.width, self.height))
        """ Draw square borders """
        for i in range(self.num_rows + 1):
            pos = (i * self.size, 0, 1, self.height)
            rect(self.display, BLACK, pos)
        for i in range(self.num_rows):
            pos = (0, i * self.size, self.width, 1)
            rect(self.display, BLACK, pos)

    def add_square(self, row, coloum, color):
        square = GrowingSquare(color, row, coloum, self.size)
        square.draw(self.display)
        self.squares.append(square)

    def delete_square(self, row, coloum, color):
        square = PeteringSquare(color, row, coloum, self.size)
        square.draw(self.display)
        self.squares.append(square)

    def update(self):
        """ Updates all the squares with animations """
        new_squares = []
        for square in self.squares:
            if square.is_animated and not square.finished_anim():
                square.change_anim()
                square.draw(self.display)
                new_squares.append(square)
        self.squares = new_squares

    def clicked(self, mouse_pos):
        return Rect(0, 0, self.width, self.height).collidepoint(mouse_pos)


class Menu:
    def __init__(self, display, size_change_callback, start_callback):
        self.display = display
        self.size_change_callback = size_change_callback
        self.start_callback = start_callback
        self.draw()

    def draw(self):
        """ Draws the menu onto the screen """
        # Button connector 0-1-2-3-4-5 (The dashes in between)
        rect(self.display, (32, 178, 170), (870, 410, 280, 15))

        # Actual buttons
        self.sizes = [Button(40, 35, DEFAULT_COLOR, 860 + x * 50, 400, str(x)) for x in range(6)]
        self.sizes[1].change_color(self.display, SELECTED_COLOR)
        for btn in self.sizes:
            btn.draw(self.display)

        self.start = Button(150, 50, DEFAULT_COLOR, 920, 200, "Start")
        self.start.draw(self.display)

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        pos = pygame.mouse.get_pos()

        for i, btn in enumerate(self.sizes):
            # Change board size
            if btn.clicked(pos):
                for bt in self.sizes:
                    bt.change_color(self.display, DEFAULT_COLOR)
                btn.change_color(self.display, SELECTED_COLOR)
                self.size_change_callback(i)

        if self.start.clicked(pos):
            self.start_callback()
