import pygame
from constants import *


class Board:
    def __init__(self, x, y, size=BOARD_SIZE):
        self.x = x
        self.y = y
        self.size = size
        self.ships = []
        self.shots = set()
        self.hits = set()
        self.owner_name = ""

    def set_owner(self, name):
        self.owner_name = name

    def draw_grid(self, screen):
        # Tlo planszy
        pygame.draw.rect(screen, OCEAN_DARK,
                         (self.x, self.y, self.size * CELL_SIZE, self.size * CELL_SIZE))

        # Linie siatki
        for i in range(self.size + 1):
            pygame.draw.line(screen, WHITE,
                             (self.x + i * CELL_SIZE, self.y),
                             (self.x + i * CELL_SIZE, self.y + self.size * CELL_SIZE), 1)
            pygame.draw.line(screen, WHITE,
                             (self.x, self.y + i * CELL_SIZE),
                             (self.x + self.size * CELL_SIZE, self.y + i * CELL_SIZE), 1)

        # Ramka
        pygame.draw.rect(screen, PEARL,
                         (self.x - 2, self.y - 2,
                          self.size * CELL_SIZE + 4,
                          self.size * CELL_SIZE + 4), 2)

        font = pygame.font.Font(None, 24)

        # Nazwa planszy
        name_text = font.render(self.owner_name, True, WHITE)
        name_rect = name_text.get_rect(center=(self.x + self.size * CELL_SIZE // 2, self.y - 25))
        screen.blit(name_text, name_rect)

        # Oznaczenia kolumn (A-J)
        for i in range(self.size):
            letter = chr(65 + i)
            text = font.render(letter, True, WHITE)
            text_rect = text.get_rect(center=(self.x + i * CELL_SIZE + CELL_SIZE // 2, self.y - 15))
            screen.blit(text, text_rect)

        # Oznaczenia wierszy (0-9)
        for i in range(self.size):
            text = font.render(str(i), True, WHITE)
            text_rect = text.get_rect(center=(self.x - 20, self.y + i * CELL_SIZE + CELL_SIZE // 2))
            screen.blit(text, text_rect)

    def draw_shots(self, screen):
        for x, y in self.shots:
            center_x = self.x + x * CELL_SIZE + CELL_SIZE // 2
            center_y = self.y + y * CELL_SIZE + CELL_SIZE // 2

            if (x, y) in self.hits:
                pygame.draw.circle(screen, RED, (center_x, center_y), CELL_SIZE // 3)
                pygame.draw.circle(screen, DARK_RED, (center_x, center_y), CELL_SIZE // 4)
                pygame.draw.line(screen, BLACK, (center_x - 6, center_y - 6),
                                 (center_x + 6, center_y + 6), 2)
                pygame.draw.line(screen, BLACK, (center_x + 6, center_y - 6),
                                 (center_x - 6, center_y + 6), 2)
            else:
                pygame.draw.circle(screen, LIGHT_GRAY, (center_x, center_y), 3)

    def receive_shot(self, x, y):
        if (x, y) in self.shots:
            return "already_shot"

        self.shots.add((x, y))

        for ship in self.ships:
            if ship.hit(x, y):
                self.hits.add((x, y))
                return "hit"

        return "miss"

    def get_cell_from_pixel(self, pixel_x, pixel_y):
        if (self.x <= pixel_x <= self.x + self.size * CELL_SIZE and
                self.y <= pixel_y <= self.y + self.size * CELL_SIZE):
            grid_x = (pixel_x - self.x) // CELL_SIZE
            grid_y = (pixel_y - self.y) // CELL_SIZE
            return int(grid_x), int(grid_y)
        return None, None

    def can_place_ship(self, ship, x, y):
        if ship.is_horizontal:
            if x < 0 or x + ship.length > self.size or y < 0 or y >= self.size:
                return False
        else:
            if x < 0 or x >= self.size or y < 0 or y + ship.length > self.size:
                return False

        positions = []
        for i in range(ship.length):
            if ship.is_horizontal:
                positions.append((x + i, y))
            else:
                positions.append((x, y + i))

        for pos in positions:
            for existing_ship in self.ships:
                if pos in existing_ship.positions:
                    return False

            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    check_x, check_y = pos[0] + dx, pos[1] + dy
                    if 0 <= check_x < self.size and 0 <= check_y < self.size:
                        for existing_ship in self.ships:
                            if (check_x, check_y) in existing_ship.positions:
                                return False

        return True

    def place_ship(self, ship, x, y):
        if self.can_place_ship(ship, x, y):
            ship.place(x, y, ship.is_horizontal)
            self.ships.append(ship)
            return True
        return False

    def all_ships_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)

    def reset(self):
        self.ships.clear()
        self.shots.clear()
        self.hits.clear()