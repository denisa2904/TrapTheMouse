"""
    This module contains the functions for drawing and checking if a button is clicked.
"""
import pygame


def is_button_clicked(x, y, button):
    """
        Checks if a button is clicked.
        :param x: x coordinate of the mouse
        :param y: y coordinate of the mouse
        :param button: the button to be checked
        :return: True if the button is clicked, False otherwise
    """
    if button.collidepoint(x, y):
        return True
    return False


def draw_button(surface, button_rect, text, text_position, rect_color, text_color):
    """
        Draws a button.
        :param surface: surface of the pygame window
        :param button_rect: the button to be drawn
        :param text: the text to be displayed on the button
        :param text_position: the position of the text
        :param rect_color: the color of the button
        :param text_color: the color of the text
        :return: draws a button
    """
    pygame.font.init()
    font_path = pygame.font.match_font("comicsansms")
    font1 = pygame.font.Font(font_path, 24)
    pygame.draw.rect(surface, rect_color, button_rect)
    button_text = font1.render(text, True, text_color)
    surface.blit(button_text, text_position)
