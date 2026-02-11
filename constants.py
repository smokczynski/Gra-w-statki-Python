import pygame

# Wymiary ekranu
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000

# Kolory - czysta, profesjonalna paleta
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
BLUE = (0, 100, 200)
LIGHT_BLUE = (100, 200, 255)
DARK_BLUE = (0, 0, 139)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 139, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GOLD = (255, 215, 0)

# Morskie kolory
OCEAN_DARK = (8, 28, 61)
OCEAN_MID = (12, 44, 86)
OCEAN_LIGHT = (26, 71, 111)
OCEAN_WAVE = (56, 116, 155)
PEARL = (253, 245, 230)

# Efekty
HIT = (220, 20, 60)
MISS = (176, 224, 230)
EXPLOSION = (255, 140, 0)
SPLASH = (173, 216, 230)

# Parametry planszy - OPTYMALNE ROZMIESZCZENIE
BOARD_SIZE = 10
CELL_SIZE = 40

# Plansza gracza - lewa strona
BOARD_OFFSET_X = 100
BOARD_OFFSET_Y = 150

# Plansza AI - prawa strona, duży odstęp
BOARD2_OFFSET_X = 950
BOARD2_OFFSET_Y = 150

# Panel statków - idealnie na środku, między planszami
PANEL_X = 550
PANEL_Y = 150
PANEL_WIDTH = 300
PANEL_HEIGHT = 500

# Pasek statusu
STATUS_BAR_WIDTH = 300
STATUS_BAR_HEIGHT = 25
STATUS_BAR_Y_OFFSET = 550

# Komunikaty
MESSAGE_X = SCREEN_WIDTH // 2
MESSAGE_Y = 50
MESSAGE_WIDTH = 600
MESSAGE_HEIGHT = 60

# Przyciski menu
MENU_BUTTON_WIDTH = 300
MENU_BUTTON_HEIGHT = 70
MENU_BUTTON_SPACING = 100

# Statki
SHIP_SIZES = {
    'Lotniskowiec': 4,
    'Krazownik': 3,
    'Niszczyciel': 2,
    'Okret podwodny': 1,
    'Okret podwodny 2': 1
}

SHIP_COLORS = {
    4: (110, 50, 20),   # Ciemny braz
    3: (70, 70, 90),    # Ciemnoszary
    2: (0, 90, 90),     # Ciemny turkus
    1: (45, 25, 75)     # Ciemny fiolet
}

# FPS
FPS = 60

# Poziomy trudnosci
DIFFICULTY_LEVELS = {
    'easy': 'LATWY',
    'medium': 'SREDNI',
    'hard': 'TRUDNY'
}