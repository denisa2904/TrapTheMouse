"""
    This module contains the GameBoard class.
"""
import random

import pygame

from objects.hexagon import Hexagon
from helpers.button import draw_button
from helpers.text import write_turn

WIDTH, HEIGHT = 900, 630
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREEN = (43, 175, 98)


class GameBoard:
    """
        This class represents the game board.
    """

    def __init__(self, rows, cols):
        """
            Initializes the GameBoard class.
            :param rows: number of rows
            :param cols:  number of columns
        """
        self.rows = rows
        self.cols = cols
        self.matrix = [[Hexagon(25, i, j) for i in range(cols)] for j in range(rows)]
        self.matrix[5][5].set_mouse()
        self.random_obstacles()
        self.back_button = pygame.Rect(30, 570, 100, 40)
        self.reset_button = pygame.Rect(30, 520, 100, 40)
        self.trapper_turn = True

    def random_obstacles(self):
        """
            Sets random obstacles on the game board.
            :return: sets random obstacles on the game board
        """
        n = random.randint(3, 7)
        for i in range(n):
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if not self.matrix[row][col].is_mouse and not self.matrix[row][col].is_obstacle:
                self.matrix[row][col].set_obstacle()
            else:
                n += 1

    def draw(self, surface):
        """
            Draws the game board (matrix of hexagons).
            :param surface: surface of the pygame window
            :return: draws a matrix of hexagons and a back button
        """
        for row in range(self.rows):
            for col in range(self.cols):
                self.matrix[row][col].draw(surface)
        draw_button(surface, self.back_button, 'Back', (50, 570), (255, 255, 255), (0, 0, 0))
        draw_button(surface, self.reset_button, 'Reset', (50, 520), (0, 0, 0), (255, 255, 255))
        if self.trapper_turn:
            pygame.draw.rect(surface, LIGHT_GREEN, (WIDTH / 2 - 100, 570, 250, 50))
            write_turn("Trapper's turn", surface, WHITE)
        else:
            pygame.draw.rect(surface, LIGHT_GREEN, (WIDTH / 2 - 100, 570, 250, 50))
            write_turn("Mouse's turn", surface, BLACK)

    def get_hexagon(self, x, y):
        """
            Gets the hexagon at the given coordinates.
            :param x: x coordinate of the hexagon
            :param y: y coordinate of the hexagon
            :return: the row and column of the hexagon
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if col == 0:
                    if row % 2 == 0 and x < 337 or row % 2 == 1 and x < 357:
                        break
                if self.matrix[row][col].is_inside(x, y):
                    return row, col
        return -1, -1
