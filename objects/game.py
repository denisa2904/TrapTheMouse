"""
    This module contains the Game class.
"""
import random
from collections import deque

import pygame

from objects.game_board import GameBoard
from helpers.text import win
from objects.menu import Menu
from helpers.button import is_button_clicked

LIGHT_GREEN = (43, 175, 98)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 900, 630
MENU_WIDTH, MENU_HEIGHT = 700, 500
MOVES_ODD_ROW = [(0, 1), (0, -1), (-1, 0), (-1, 1), (1, 0), (1, 1)]
MOVES_EVEN_ROW = [(0, 1), (0, -1), (-1, 0), (-1, -1), (1, 0), (1, -1)]


class Game:
    """
        This class represents the game.
    """

    def __init__(self):
        """
            Initializes the Game class.
        """
        self.board = GameBoard(11, 11)
        self.menu = Menu()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.menu_screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
        pygame.display.set_caption("Trap the Mouse")

        self.menu_active = True
        self.start_game = False
        self.running = True
        self.selector_active = False
        self.play = False

        self.ai_level = 0
        self.is_human_opponent = False
        self.trapper_turn = True

        self.mouse_position = (5, 5)
        self.moves = MOVES_ODD_ROW
        self.ai_levels ={
            1: self.ai_easy_mouse_move,
            2: self.ai_medium_mouse_move,
            3: self.ai_hard_mouse_move
        }

    def check_win(self):
        """
            Checks if the trapper or the mouse won.
            :return: True if someone won, False otherwise
        """
        if self.mouse_position[0] == 0 or self.mouse_position[0] == self.board.rows - 1 or \
                self.mouse_position[1] == 0 or self.mouse_position[1] == self.board.cols - 1:
            win("Mouse", self.screen)
            self.play = False
            self.menu_active = True
            self.back_menu()
        else:
            for move in self.moves:
                row = self.mouse_position[0] + move[0]
                col = self.mouse_position[1] + move[1]
                if not self.board.matrix[row][col].is_obstacle:
                    return False
            win("Trapper", self.screen)
            self.play = False
            self.menu_active = True
            self.back_menu()
            self.ai_level = 0
        return True

    def reset(self):
        """
            Resets the game.
            :return: resets the game
        """
        self.board = GameBoard(11, 11)
        self.mouse_position = (5, 5)
        self.start_game = True
        self.play = False
        self.trapper_turn = True


    def mouse_select(self, row, col):
        """
        Selects the mouse.
        :param row: row of the mouse
        :param col: column of the mouse
        :return: selects the mouse and updates the mouse position
        """
        self.board.matrix[self.mouse_position[0]][self.mouse_position[1]].is_mouse = False
        self.board.matrix[row][col].set_mouse()
        self.mouse_position = (row, col)
        self.trapper_turn = True
        self.board.trapper_turn = True

    def trapper_move(self, x, y):
        """
            Moves for the one who wants to trap the mouse.
            :param x: x coordinate of the mouse click
            :param y: y coordinate of the mouse click
            :return: plays the game vs human
        """
        if self.check_win():
            return
        row, col = self.board.get_hexagon(x, y)
        if (row == -1 or col == -1) or (
                self.board.matrix[row][col].is_obstacle or self.board.matrix[row][col].is_mouse):
            return
        self.board.matrix[row][col].set_obstacle()
        self.board.matrix[row][col].is_obstacle = True
        self.trapper_turn = False
        self.board.trapper_turn = False
        self.board.draw(self.screen)
        if self.check_win():
            return

    def mouse_move(self, x, y):
        """
            Human opponent moves the mouse by clicking a hexagon.
            :param x: x coordinate of the mouse click
            :param y: y coordinate of the mouse click
            :return: plays the game vs human
        """
        if self.check_win():
            return
        pygame.display.flip()
        if self.mouse_position[0] % 2 == 1:
            self.moves = MOVES_ODD_ROW
        else:
            self.moves = MOVES_EVEN_ROW
        row, col = self.board.get_hexagon(x, y)
        if (row == -1 or col == -1) or (
                self.board.matrix[row][col].is_obstacle or self.board.matrix[row][col].is_mouse):
            return

        row_diff = row - self.mouse_position[0]
        col_diff = col - self.mouse_position[1]
        if (row_diff, col_diff) in self.moves:
            self.mouse_select(row, col)

        self.board.draw(self.screen)
        if self.check_win():
            return

    def ai_easy_mouse_move(self):
        """
            Easy AI opponent that makes random moves.
            :return: moves the mouse
        """
        if self.check_win():
            return
        pygame.display.flip()
        if self.mouse_position[0] % 2 == 1:
            self.moves = MOVES_ODD_ROW
        else:
            self.moves = MOVES_EVEN_ROW

        row, col = self.random_move()
        self.mouse_select(row, col)
        self.board.draw(self.screen)
        if self.check_win():
            return

    def ai_medium_mouse_move(self):
        """
            Medium AI opponent that makes random moves 70% of the time and best moves 30% of the time.
            :return: moves the mouse
        """
        if self.check_win():
            return
        pygame.display.flip()
        if self.mouse_position[0] % 2 == 1:
            self.moves = MOVES_ODD_ROW
        else:
            self.moves = MOVES_EVEN_ROW
        chance = random.randint(1, 10)
        if chance <= 4:
            move = self.random_move()
            row, col = move[0], move[1]
        else:
            move = self.choose_best_move()
            row, col = self.mouse_position[0] + move[0], self.mouse_position[1] + move[1]
        self.mouse_select(row, col)
        self.board.draw(self.screen)
        if self.check_win():
            return

    def ai_hard_mouse_move(self):
        """
            Hard AI opponent that makes the best moves.
            :return: moves the mouse
        """
        if self.check_win():
            return
        pygame.display.flip()
        if self.mouse_position[0] % 2 == 1:
            self.moves = MOVES_ODD_ROW
        else:
            self.moves = MOVES_EVEN_ROW
        move = self.choose_best_move()
        row, col = self.mouse_position[0] + move[0], self.mouse_position[1] + move[1]
        self.mouse_select(row, col)
        self.board.draw(self.screen)
        if self.check_win():
            return

    def back_menu(self):
        """
            Goes back to the menu.
            :return: goes back to the menu
        """
        self.reset()
        self.menu_active = True
        self.start_game = False
        self.is_human_opponent = False
        pygame.init()
        self.menu_screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
        pygame.display.set_caption("Trap the Mouse")
        self.menu.draw_menu(self.menu_screen)
        pygame.display.flip()

    def random_move(self):
        """
            Returns a random move.
            :return: a random move
        """
        row, col = self.mouse_position
        while True:
            move = random.choice(self.moves)
            new_row, new_col = row + move[0], col + move[1]
            if (not self.board.matrix[new_row][new_col].is_obstacle and
                    not self.board.matrix[new_row][new_col].is_mouse):
                return new_row, new_col

    def choose_best_move(self):
        """
            Calculates the best move based on distance to edge
            :return: the best move
        """
        if self.mouse_position[0] % 2 == 1:
            moves = MOVES_ODD_ROW
        else:
            moves = MOVES_EVEN_ROW
        best_move = None
        best_distance = float('inf')
        distances = self.bfs_distances_from_edges()
        for move in moves:
            row = self.mouse_position[0] + move[0]
            col = self.mouse_position[1] + move[1]
            if not self.board.matrix[row][col].is_obstacle and not self.board.matrix[row][col].is_mouse:
                if distances[row][col] <= best_distance:
                    best_distance = distances[row][col]
                    best_move = move
        return best_move

    def bfs_distances_from_edges(self):
        """
            Calculates the distances from the edges to the mouse position using BFS
            :return: a matrix where each cell contains the distance from the edges
        """
        target_row, target_col = self.mouse_position
        rows, cols = self.board.rows, self.board.cols
        distances = [[float('inf')] * cols for _ in range(rows)]
        visited = [[False] * cols for _ in range(rows)]
        queue = deque()

        for i in range(rows):
            for j in range(cols):
                if i == 0 or i == rows - 1 or j == 0 or j == cols - 1:
                    queue.append((i, j, 0))
                    visited[i][j] = True

        while queue:
            current_row, current_col, distance = queue.popleft()
            distances[current_row][current_col] = distance
            if current_row % 2 == 0:
                directions = MOVES_EVEN_ROW
            else:
                directions = MOVES_ODD_ROW
            neighbors = [(current_row + i, current_col + j) for i, j in directions]
            if not (target_row, target_col) in neighbors:
                for neighbor_row, neighbor_col in neighbors:
                    if (0 <= neighbor_row < rows and 0 <= neighbor_col < cols
                            and not visited[neighbor_row][neighbor_col]
                            and not self.board.matrix[neighbor_row][neighbor_col].is_obstacle):
                        queue.append((neighbor_row, neighbor_col, distance + 1))
                        visited[neighbor_row][neighbor_col] = True

        return distances

    def handle_menu_buttons(self, x, y):
        """
            Handles the menu buttons.
            :param x: x coordinate of the mouse click
            :param y: y coordinate of the mouse click
            :return: starts the game with human opponent or opens the AI level selector
        """
        if is_button_clicked(x, y, self.menu.first_button):
            self.selector_active = True
            self.menu_active = False
        elif is_button_clicked(x, y, self.menu.second_button):
            self.reset()
            self.menu_active = False
            self.is_human_opponent = True
            pygame.time.wait(200)

    def handle_selector_buttons(self, x, y):
        """
            Handles the AI level selector buttons.
            :param x: x coordinate of the mouse click
            :param y: y coordinate of the mouse click
            :return: sets the AI level according to the button clicked
        """
        if is_button_clicked(x, y, self.menu.first_button):
            self.start_game = True
            self.selector_active = False
            self.ai_level = 1
            pygame.time.wait(200)
        elif is_button_clicked(x, y, self.menu.second_button):
            self.start_game = True
            self.selector_active = False
            self.ai_level = 2
            pygame.time.wait(200)
        elif is_button_clicked(x, y, self.menu.third_button):
            self.start_game = True
            self.selector_active = False
            self.ai_level = 3
            pygame.time.wait(200)

    def handle_game_buttons(self, x, y):
        """
            Handles the game buttons.
            :param x: x coordinate of the mouse click
            :param y: y coordinate of the mouse click
            :return: handles the game buttons
        """
        if is_button_clicked(x, y, self.board.back_button):
            self.back_menu()
        if is_button_clicked(x, y, self.board.reset_button):
            self.reset()

    def handle_start_game(self):
        """
            Handles the start of the game.
            :return: opens the game window and draws the game board
        """
        self.reset()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Trap the Mouse")
        screen.fill(LIGHT_GREEN)
        self.play = True
        self.start_game = False
        self.board.draw(self.screen)
        pygame.display.flip()

    def run(self):
        """
            Runs the game.
            :return: runs the game
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    if not self.start_game:
                        if self.menu_active:
                            self.handle_menu_buttons(x, y)

                        elif self.selector_active:
                            self.handle_selector_buttons(x, y)

                        elif self.play:
                            self.handle_game_buttons(x, y)
                            if self.trapper_turn:
                                self.board.trapper_turn = True
                                self.trapper_move(x, y)
                            else:
                                self.board.trapper_turn = False
                                if self.is_human_opponent:
                                    self.mouse_move(x, y)

            if not self.is_human_opponent and not self.trapper_turn:
                if self.ai_level in self.ai_levels:
                    self.ai_levels[self.ai_level]()

            if self.selector_active:
                self.menu.draw_ai_level_selector(self.menu_screen)
                pygame.display.flip()
                continue

            if self.menu_active:
                self.menu.draw_menu(self.menu_screen)
                pygame.display.flip()
                continue

            if self.start_game:
                self.handle_start_game()
                continue

            if self.play:
                self.board.draw(self.screen)
                pygame.display.flip()
                continue

            pygame.display.flip()

        pygame.quit()
