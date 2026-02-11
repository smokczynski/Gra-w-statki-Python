import random
import pygame
from constants import *


class AI:
    def __init__(self, name="KOMPUTER", difficulty='medium'):
        self.name = name
        self.difficulty = difficulty
        self.board = None
        self.opponent_board = None
        self.last_hits = []
        self.target_stack = []
        self.hunt_mode = False
        self.ready = True

    def init_board(self, x, y):
        from board import Board
        self.board = Board(x, y)
        self.board.set_owner(self.name)
        self._auto_place_ships()

    def _auto_place_ships(self):
        from ship import create_default_ships
        ships = create_default_ships()

        for ship in ships:
            placed = False
            attempts = 0
            while not placed and attempts < 1000:
                x = random.randint(0, self.board.size - 1)
                y = random.randint(0, self.board.size - 1)
                ship.is_horizontal = random.choice([True, False])

                if self.board.place_ship(ship, x, y):
                    placed = True
                attempts += 1

    def take_turn(self):
        if self.difficulty == 'easy':
            return self._easy_move()
        elif self.difficulty == 'hard':
            return self._hard_move()
        else:
            return self._medium_move()

    def _easy_move(self):
        attempts = 0
        while attempts < 100:
            x = random.randint(0, self.opponent_board.size - 1)
            y = random.randint(0, self.opponent_board.size - 1)

            if (x, y) not in self.opponent_board.shots:
                result = self.opponent_board.receive_shot(x, y)
                if result == "hit":
                    self.last_hits.append((x, y))
                return result, (x, y)
            attempts += 1
        return "miss", (0, 0)

    def _medium_move(self):
        if self.hunt_mode and self.target_stack:
            x, y = self.target_stack.pop(0)
            if (x, y) not in self.opponent_board.shots:
                result = self.opponent_board.receive_shot(x, y)

                if result == "hit":
                    self._add_adjacent_targets(x, y)
                    self.last_hits.append((x, y))
                elif not self.target_stack:
                    self.hunt_mode = False

                return result, (x, y)
            else:
                return self._medium_move()
        else:
            return self._easy_move()

    def _hard_move(self):
        for x in range(self.opponent_board.size):
            for y in range(self.opponent_board.size):
                if (x + y) % 2 == 0:
                    if (x, y) not in self.opponent_board.shots:
                        result = self.opponent_board.receive_shot(x, y)
                        if result == "hit":
                            self._add_adjacent_targets(x, y)
                            self.hunt_mode = True
                            self.last_hits.append((x, y))
                        return result, (x, y)

        return self._medium_move()

    def _add_adjacent_targets(self, x, y):
        self.hunt_mode = True
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        if len(self.last_hits) >= 2:
            x1, y1 = self.last_hits[-2]
            x2, y2 = self.last_hits[-1]
            dx = x2 - x1
            dy = y2 - y1

            if dx != 0 or dy != 0:
                nx, ny = x2 + dx, y2 + dy
                if (0 <= nx < self.opponent_board.size and
                        0 <= ny < self.opponent_board.size and
                        (nx, ny) not in self.opponent_board.shots and
                        (nx, ny) not in self.target_stack):
                    self.target_stack.insert(0, (nx, ny))

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.opponent_board.size and
                    0 <= ny < self.opponent_board.size and
                    (nx, ny) not in self.opponent_board.shots and
                    (nx, ny) not in self.target_stack):
                self.target_stack.append((nx, ny))

    def draw(self, screen, show_ships=False):
        if self.board:
            self.board.draw_grid(screen)

            if show_ships:
                for ship in self.board.ships:
                    ship.draw(screen, self.board.x, self.board.y, hide=False)
            else:
                for ship in self.board.ships:
                    if ship.is_sunk():
                        ship.draw(screen, self.board.x, self.board.y, hide=False)

            self.board.draw_shots(screen)