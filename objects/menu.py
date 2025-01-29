"""
    This module contains the Menu class.
"""
import pygame
from helpers.button import draw_button

WIDTH, HEIGHT = 700, 500
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
LIGHT_GREEN = (100, 128, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Menu:
    """
        This class represents the menu.
    """

    def __init__(self):
        """
            Initializes the Menu class.
        """
        self.first_button = pygame.Rect((WIDTH - BUTTON_WIDTH) / 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.second_button = pygame.Rect((WIDTH - BUTTON_WIDTH) / 2, 300, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.third_button = pygame.Rect((WIDTH - BUTTON_WIDTH) / 2, 400, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.background_image = pygame.image.load("../public/menu_photo.png")
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))

    def draw_menu(self, surface):
        """
            Draws the menu.
            :param surface: surface of the pygame window
            :return: draws the menu
        """

        surface.blit(self.background_image, [0, 0])

        pygame.font.init()
        font_path = pygame.font.match_font("comicsansms")
        font = pygame.font.Font(font_path, 36)
        text = font.render("Trap the Mouse", True, WHITE)
        surface.blit(text, (215, 100))

        draw_button(surface, self.first_button, "Play vs AI", (WIDTH / 2 - 55, 210), BLACK, LIGHT_GREEN)

        draw_button(surface, self.second_button, "Play vs Human", (WIDTH / 2 - 75, 310), LIGHT_GREEN, BLACK)

    def draw_ai_level_selector(self, surface):
        """
            Draws the AI level selector.
            :param surface: surface of the pygame window
            :return: draws the AI level selector
        """
        surface.blit(self.background_image, [0, 0])

        pygame.font.init()
        font_path = pygame.font.match_font("comicsansms")
        font = pygame.font.Font(font_path, 36)
        text = font.render("Select AI level", True, WHITE)
        surface.blit(text, (215, 100))

        draw_button(surface, self.first_button, "Easy", (WIDTH / 2 - 30, 210), BLACK, LIGHT_GREEN)
        draw_button(surface, self.second_button, "Medium", (WIDTH / 2 - 50, 310), LIGHT_GREEN, BLACK)
        draw_button(surface, self.third_button, "Hard", (WIDTH / 2 - 30, 410), BLACK, LIGHT_GREEN)
