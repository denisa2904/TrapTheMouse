"""
    This module contains functions that write text on the pygame window.
"""
import pygame

WIDTH, HEIGHT = 900, 630
LIGHT_GREEN = (43, 175, 98)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def win(player, surface):
    """
        Announces the winner.
        :param player: the winner
        :param surface: surface of the pygame window
        :return: writes who won
    """
    pygame.display.flip()
    pygame.font.init()
    font_path = pygame.font.match_font("comicsansms")
    font = pygame.font.Font(font_path, 36)
    text = font.render(f"{player} won!", True, BLACK)
    surface.blit(text, (50, 100))
    pygame.display.flip()
    print(f"{player} won!")
    pygame.time.wait(2000)


def write_turn(turn, surface, color):
    """
        Writes whose turn it is.
        :param turn: "Trapper" or "Mouse"
        :param surface: surface of the pygame window
        :param color: color of the text
        :return: writes whose turn it is at the bottom of the window
    """
    pygame.font.init()
    font_path = pygame.font.match_font("comicsansms")
    font = pygame.font.Font(font_path, 36)
    text = font.render(turn, True, color)
    surface.blit(text, (WIDTH / 2 - 100, 570))
