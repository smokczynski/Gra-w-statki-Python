import pygame
from constants import *


class Ship:
    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.positions = []
        self.hits = set()
        self.is_horizontal = True
        self.color = SHIP_COLORS[length]
        self.is_dragging = False
        self.placed = False

    def place(self, x, y, is_horizontal):
        self.is_horizontal = is_horizontal
        self.positions = []

        for i in range(self.length):
            if is_horizontal:
                self.positions.append((x + i, y))
            else:
                self.positions.append((x, y + i))
        self.placed = True

    def hit(self, x, y):
        if (x, y) in self.positions and (x, y) not in self.hits:
            self.hits.add((x, y))
            return True
        return False

    def is_sunk(self):
        return len(self.hits) == self.length

    def draw(self, screen, offset_x, offset_y, hide=False):
        if hide and not self.is_sunk():
            return

        for i, (x, y) in enumerate(self.positions):
            pixel_x = offset_x + x * CELL_SIZE
            pixel_y = offset_y + y * CELL_SIZE
            rect = pygame.Rect(pixel_x + 2, pixel_y + 2, CELL_SIZE - 4, CELL_SIZE - 4)

            if (x, y) in self.hits:
                if self.is_sunk():
                    pygame.draw.rect(screen, DARK_GRAY, rect, 2, border_radius=3)
                else:
                    pygame.draw.rect(screen, HIT, rect, border_radius=3)
                    pygame.draw.circle(screen, BLACK,
                                       (pixel_x + CELL_SIZE // 2, pixel_y + CELL_SIZE // 2), 3)
            else:
                pygame.draw.rect(screen, self.color, rect, border_radius=3)
                pygame.draw.rect(screen, BLACK, rect, 1, border_radius=3)

    def draw_dragging(self, screen, mouse_x, mouse_y):
        if self.is_horizontal:
            width = self.length * CELL_SIZE
            height = CELL_SIZE
        else:
            width = CELL_SIZE
            height = self.length * CELL_SIZE

        s = pygame.Surface((width, height), pygame.SRCALPHA)
        s.fill((*self.color, 180))
        rect = pygame.Rect(mouse_x - width // 2, mouse_y - height // 2, width, height)
        screen.blit(s, rect)
        pygame.draw.rect(screen, WHITE, rect, 2, border_radius=5)


def create_default_ships():
    return [
        Ship("Lotniskowiec", 4),
        Ship("Krazownik", 3),
        Ship("Niszczyciel", 2),
        Ship("Okret podwodny", 1),
        Ship("Okret podwodny 2", 1)
    ]