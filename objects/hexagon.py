"""
    This module contains the Hexagon class.
"""
import math
import pygame

width, height = 900, 630
BORDER_COLOR_DARK_GREEN = (21, 87, 49)
FILL_COLOR_GREEN = (32, 131, 74)
BORDER_COLOR_DARK_BROWN = (135, 62, 35)
FILL_COLOR_BROWN = '#935139'
IMAGE = pygame.image.load("../public/mouse1.png")
IMAGE_SIZE = (50, 50)
IMAGE = pygame.transform.scale(IMAGE, IMAGE_SIZE)


class Hexagon:
    """
        This class represents a hexagon.
    """

    def __init__(self, radius, row, col):
        """
            Initializes the Hexagon class.
            :param radius: the radius of the hexagon
            :param row: the row of the hexagon
            :param col: the column of the hexagon
        """
        self.radius = radius
        self.width = math.sqrt(3) * radius + 1.7
        self.height = 2 * radius - 8
        self.row = row
        self.col = col
        self.x = row * self.width + width * 0.4
        self.y = col * self.height + height / 10
        if col % 2 == 1:
            self.x += self.height / 2
        self.is_obstacle = False
        self.is_mouse = False
        self.points = []
        for i in range(6):
            angle = math.radians(60 * i)
            hx = self.x + self.radius * math.sin(angle)
            hy = self.y + self.radius * math.cos(angle)
            self.points.append((hx, hy))

    def set_obstacle(self):
        """
            Sets the hexagon as an obstacle.
            :return: sets the hexagon as an obstacle
        """
        self.is_obstacle = True

    def set_mouse(self):
        """
            Sets the hexagon as the mouse.
            :return: sets the hexagon as the mouse
        """
        self.is_mouse = True

    def is_inside(self, x, y):
        """
            Checks if a point is inside the hexagon.
            :param x: x coordinate of the point
            :param y: y coordinate of the point
            :return: True if the point is inside the hexagon, False otherwise
        """
        inside = False
        n = len(self.points)
        j = n - 1
        for i in range(n - 1):
            if ((self.points[i][1] > y) != (self.points[j][1] > y)
                    and (x < (self.points[j][0] - self.points[i][0]) *
                         (y - self.points[i][1]) / (self.points[j][1] - self.points[i][1])
                         + self.points[i][0])):
                inside = not inside
            j = i

        return inside

    def draw(self, surface):
        """
            Draws a hexagon.
            :param surface: surface of the pygame window
            :return: draws a hexagon
        """
        if self.is_obstacle:
            pygame.draw.polygon(surface, FILL_COLOR_BROWN, self.points, 0)
            pygame.draw.polygon(surface, BORDER_COLOR_DARK_BROWN, self.points, 6)
        else:
            pygame.draw.polygon(surface, FILL_COLOR_GREEN, self.points, 0)
            pygame.draw.polygon(surface, BORDER_COLOR_DARK_GREEN, self.points, 6)

        if self.is_mouse:
            surface.blit(pygame.transform.scale(IMAGE, IMAGE_SIZE), (self.x - self.radius, self.y - self.radius))
