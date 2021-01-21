import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Square:
    def __init__(self, color, row, coloum, animated, row_size):
        self.color = color
        self.row = row
        self.coloum = coloum
        self.animated = animated
        self.size = row_size

    def draw(self, display):
        start_x = self.size * self.coloum
        start_y = self.size * self.row
        rect = (start_x + 1, start_y + 1, self.size - 1, self.size - 1)
        pygame.draw.rect(display, self.color, rect)

    def erase(self, display):
        start_x = self.size * self.coloum
        start_y = self.size * self.row
        rect = (start_x + 1, start_y + 1, self.size - 1, self.size - 1)
        pygame.draw.rect(display, WHITE, rect)

    def is_animated(self):
        return animated


class ChangingSizeSquares(Square):
    def __init__(self, color, row, coloum, row_size):
        Square.__init__(self, color, row, coloum, True, row_size)

    def change_anim(self):
        self.anim_state -= 1

    def finished_anim(self):
        return self.anim_state <= 0

    def draw(self, display):
        # First erase everything that was before
        self.erase(display)
        """ b_size, precentage (in decimal) that need to
        move in order to much size.
        For example, size needed is 0.6 'self.sizes[2]',
        take 0.2 from the left, and same from the right """
        b_size = (1 - self.sizes[self.anim_state]) / 2
        if self.sizes[self.anim_state] == 0:
            return
        start_x = self.size * self.coloum + self.size * b_size
        start_y = self.size * self.row + self.size * b_size
        size_x = self.size - self.size * b_size * 2
        size_y = self.size - self.size * b_size * 2
        rect = (start_x + 1, start_y + 1, size_x - 1, size_y - 1)
        pygame.draw.rect(display, self.color, rect)


class GrowingSquare(ChangingSizeSquares):
    def __init__(self, color, row, coloum, row_size):
        ChangingSizeSquares.__init__(self, color, row, coloum, row_size)
        self.anim_state = 9
        self.sizes = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]


class PeteringSquare(ChangingSizeSquares):
    def __init__(self, color, row, coloum, row_size):
        ChangingSizeSquares.__init__(self, color, row, coloum, row_size)
        self.anim_state = 10
        self.sizes = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
