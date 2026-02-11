import pygame
import random
from board import Board
from ship import create_default_ships
from constants import *


class Player:
    def __init__(self, name):
        self.name = name
        self.board = None
        self.opponent_board = None
        self.ships_to_place = []
        self.current_drag_ship = None
        self.selected_ship_index = 0
        self.ready = False

    def init_board(self, x, y):
        self.board = Board(x, y)
        self.board.set_owner(self.name)
        self.ships_to_place = create_default_ships()

    def handle_placement_events(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.selected_ship_index < len(self.ships_to_place):
                    ship = self.ships_to_place[self.selected_ship_index]
                    ship.is_dragging = True
                    self.current_drag_ship = ship
            elif event.button == 3:
                if self.selected_ship_index < len(self.ships_to_place):
                    ship = self.ships_to_place[self.selected_ship_index]
                    ship.is_horizontal = not ship.is_horizontal

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.current_drag_ship:
                self._try_place_ship(mouse_pos)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._auto_place_ships()
                return True
            elif event.key == pygame.K_r:
                self.board.reset()
                self.ships_to_place = create_default_ships()
                self.selected_ship_index = 0

        return False

    def _try_place_ship(self, mouse_pos):
        if not self.current_drag_ship:
            return

        grid_x, grid_y = self.board.get_cell_from_pixel(mouse_pos[0], mouse_pos[1])

        if grid_x is not None and grid_y is not None:
            if self.board.place_ship(self.current_drag_ship, grid_x, grid_y):
                self.ships_to_place.pop(self.selected_ship_index)
                self.current_drag_ship.is_dragging = False
                self.current_drag_ship = None

                if self.selected_ship_index >= len(self.ships_to_place):
                    self.selected_ship_index = max(0, len(self.ships_to_place) - 1)

                if len(self.ships_to_place) == 0:
                    self.ready = True
                return True

        if self.current_drag_ship:
            self.current_drag_ship.is_dragging = False
            self.current_drag_ship = None
        return False

    def _auto_place_ships(self):
        self.board.reset()
        self.ships_to_place = create_default_ships()

        for ship in self.ships_to_place[:]:
            placed = False
            attempts = 0
            while not placed and attempts < 1000:
                x = random.randint(0, self.board.size - 1)
                y = random.randint(0, self.board.size - 1)
                ship.is_horizontal = random.choice([True, False])

                if self.board.place_ship(ship, x, y):
                    self.ships_to_place.remove(ship)
                    placed = True
                attempts += 1

        if len(self.ships_to_place) == 0:
            self.ready = True

    def take_turn(self, mouse_pos):
        grid_x, grid_y = self.opponent_board.get_cell_from_pixel(mouse_pos[0], mouse_pos[1])

        if grid_x is not None and grid_y is not None:
            if (grid_x, grid_y) in self.opponent_board.shots:
                return "already_shot", None

            result = self.opponent_board.receive_shot(grid_x, grid_y)
            return result, (grid_x, grid_y)

        return None, None

    def draw(self, screen, show_ships=True):
        if self.board:
            self.board.draw_grid(screen)

            if show_ships:
                for ship in self.board.ships:
                    ship.draw(screen, self.board.x, self.board.y, hide=False)

            self.board.draw_shots(screen)

    def draw_placement_panel(self, screen):
        if self.ready or len(self.ships_to_place) == 0:
            return

        # Panel na srodku, miedzy planszami
        panel_x = PANEL_X
        panel_y = PANEL_Y
        panel_width = PANEL_WIDTH
        panel_height = PANEL_HEIGHT

        # Tlo panelu
        pygame.draw.rect(screen, (20, 40, 60),
                         (panel_x, panel_y, panel_width, panel_height), border_radius=10)
        pygame.draw.rect(screen, WHITE,
                         (panel_x, panel_y, panel_width, panel_height), 2, border_radius=10)

        font_title = pygame.font.Font(None, 28)
        font = pygame.font.Font(None, 24)
        font_small = pygame.font.Font(None, 20)

        # Tytul
        title_text = font_title.render("ROZMIESZCZANIE STATKOW", True, WHITE)
        title_rect = title_text.get_rect(center=(panel_x + panel_width // 2, panel_y + 30))
        screen.blit(title_text, title_rect)

        # Instrukcje
        instructions = [
            "LPM - przeciagnij statek",
            "PPM - zmien orientacje",
            "SPACJA - auto-rozmieszczenie",
            "R - reset",
            f"Pozostalo: {len(self.ships_to_place)}"
        ]

        for i, text in enumerate(instructions):
            inst_text = font_small.render(text, True, LIGHT_GRAY)
            screen.blit(inst_text, (panel_x + 20, panel_y + 80 + i * 25))

        # Lista statkow
        for i, ship in enumerate(self.ships_to_place):
            y_pos = panel_y + 250 + i * 50

            if i == self.selected_ship_index:
                pygame.draw.rect(screen, GOLD,
                                 (panel_x + 10, y_pos - 5, panel_width - 20, 40), 2, border_radius=5)

            color = GOLD if i == self.selected_ship_index else WHITE
            ship_text = font.render(f"{ship.name} ({ship.length})", True, color)
            screen.blit(ship_text, (panel_x + 20, y_pos))

            # Podglad statku
            preview_x = panel_x + 200
            preview_y = y_pos + 5

            for j in range(ship.length):
                if ship.is_horizontal:
                    rect = pygame.Rect(preview_x + j * 20, preview_y, 15, 15)
                else:
                    rect = pygame.Rect(preview_x, preview_y + j * 20, 15, 15)

                pygame.draw.rect(screen, ship.color, rect)
                pygame.draw.rect(screen, WHITE, rect, 1)

    def draw_dragging_ship(self, screen, mouse_pos):
        if self.current_drag_ship and self.current_drag_ship.is_dragging:
            self.current_drag_ship.draw_dragging(screen, mouse_pos[0], mouse_pos[1])