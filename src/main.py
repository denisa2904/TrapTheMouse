"""
    Main file for the game Trap the Mouse.
    This script starts the game.
"""

import pygame

from objects.game import Game

LIGHT_GREEN = (43, 175, 98)
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 900, 630
MENU_WIDTH, MENU_HEIGHT = 700, 500


def main():
    pygame.init()
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
