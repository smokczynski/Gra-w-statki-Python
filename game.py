import pygame
import sys
import random
from constants import *
from player import Player
from ai import AI


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("BATTLESHIP - Gra w Statki")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

        self.state = "MENU"
        self.player = None
        self.ai = None
        self.current_turn = None
        self.message = ""
        self.message_timer = 0
        self.difficulty = 'medium'
        self.winner = None

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_events(event)

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def handle_events(self, event):
        if self.state == "MENU":
            self._handle_menu_events(event)
        elif self.state == "PLACEMENT":
            self._handle_placement_events(event)
        elif self.state == "BATTLE":
            self._handle_battle_events(event)
        elif self.state == "GAME_OVER":
            self._handle_game_over_events(event)

    def _handle_menu_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.difficulty = 'easy'
                self._setup_game()
            elif event.key == pygame.K_2:
                self.difficulty = 'medium'
                self._setup_game()
            elif event.key == pygame.K_3:
                self.difficulty = 'hard'
                self._setup_game()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._check_menu_click(event.pos)

    def _check_menu_click(self, mouse_pos):
        x, y = mouse_pos
        center_x = SCREEN_WIDTH // 2

        if 350 <= y <= 420:
            if center_x - 150 <= x <= center_x + 150:
                self.difficulty = 'easy'
                self._setup_game()
        elif 470 <= y <= 540:
            if center_x - 150 <= x <= center_x + 150:
                self.difficulty = 'medium'
                self._setup_game()
        elif 590 <= y <= 660:
            if center_x - 150 <= x <= center_x + 150:
                self.difficulty = 'hard'
                self._setup_game()

    def _setup_game(self):
        self.player = Player("GRACZ")
        self.player.init_board(BOARD_OFFSET_X, BOARD_OFFSET_Y)

        ai_names = ["KOMPUTER"]
        self.ai = AI(random.choice(ai_names), self.difficulty)
        self.ai.init_board(BOARD2_OFFSET_X, BOARD2_OFFSET_Y)

        self.player.opponent_board = self.ai.board
        self.ai.opponent_board = self.player.board

        self.state = "PLACEMENT"
        self.message = "Rozmiesc swoje statki!"
        self.message_timer = 180

    def _handle_placement_events(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.player.ready:
                self.state = "BATTLE"
                self.current_turn = "player"
                self.message = "Twoja tura! Strzelaj!"
                self.message_timer = 180

        self.player.handle_placement_events(event, mouse_pos)

    def _handle_battle_events(self, event):
        if self.current_turn == "player":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                result, coords = self.player.take_turn(mouse_pos)

                if result and result != "already_shot":
                    self._process_player_shot(result, coords)

        elif self.current_turn == "ai":
            pygame.time.wait(500)
            result, coords = self.ai.take_turn()
            self._process_ai_shot(result, coords)

    def _process_player_shot(self, result, coords):
        if coords:
            x, y = coords
            coord_text = f"{chr(65 + x)},{y}"

            if result == "hit":
                sunk_ship = None
                for ship in self.ai.board.ships:
                    if ship.is_sunk() and len(ship.hits) == ship.length:
                        sunk_ship = ship
                        break

                if sunk_ship:
                    self.message = f"ZATOPIONY! {sunk_ship.name} ({coord_text})"
                else:
                    self.message = f"TRAFIONY! ({coord_text})"

                if self.ai.board.all_ships_sunk():
                    self.state = "GAME_OVER"
                    self.winner = "GRACZ"
                    self.message = "Zwyciestwo! Zatopiles wszystkie statki!"
                else:
                    self.message_timer = 120
                    return

            elif result == "miss":
                self.message = f"Pudlo! ({coord_text})"

            self.message_timer = 120

            if result != "hit" and self.state != "GAME_OVER":
                self.current_turn = "ai"
                self.message = "Tura komputera..."

    def _process_ai_shot(self, result, coords):
        if coords:
            x, y = coords
            coord_text = f"{chr(65 + x)},{y}"

            if result == "hit":
                sunk_ship = None
                for ship in self.player.board.ships:
                    if ship.is_sunk() and len(ship.hits) == ship.length:
                        sunk_ship = ship
                        break

                if sunk_ship:
                    self.message = f"Komputer zatopil {sunk_ship.name}! ({coord_text})"
                else:
                    self.message = f"Komputer trafil! ({coord_text})"

                if self.player.board.all_ships_sunk():
                    self.state = "GAME_OVER"
                    self.winner = "KOMPUTER"
                    self.message = "Porazka! Komputer zatopil wszystkie twoje statki!"
                else:
                    self.message_timer = 120
                    self.current_turn = "ai"
                    return

            elif result == "miss":
                self.message = f"Komputer spudlowal! ({coord_text})"

            self.message_timer = 120

            if self.state != "GAME_OVER":
                self.current_turn = "player"
                self.message = "Twoja tura!"

    def update(self):
        if self.message_timer > 0:
            self.message_timer -= 1

    def draw(self):
        self.screen.fill(OCEAN_DARK)

        if self.state == "MENU":
            self._draw_menu()
        elif self.state == "PLACEMENT":
            self._draw_placement()
        elif self.state == "BATTLE":
            self._draw_battle()
        elif self.state == "GAME_OVER":
            self._draw_game_over()

        pygame.display.flip()

    def _draw_menu(self):
        center_x = SCREEN_WIDTH // 2

        # Tytul
        title = self.font_large.render("BATTLESHIP", True, WHITE)
        title_rect = title.get_rect(center=(center_x, 200))
        self.screen.blit(title, title_rect)

        subtitle = self.font_medium.render("Gra w Statki", True, LIGHT_GRAY)
        subtitle_rect = subtitle.get_rect(center=(center_x, 260))
        self.screen.blit(subtitle, subtitle_rect)

        # Przyciski
        difficulties = [
            ("1 - LATWY", 350, GREEN),
            ("2 - SREDNI", 470, YELLOW),
            ("3 - TRUDNY", 590, RED)
        ]

        for text, y_pos, color in difficulties:
            button_rect = pygame.Rect(center_x - 150, y_pos, 300, 70)
            pygame.draw.rect(self.screen, DARK_BLUE, button_rect, border_radius=10)
            pygame.draw.rect(self.screen, color, button_rect, 3, border_radius=10)

            text_surf = self.font_medium.render(text, True, WHITE)
            text_rect = text_surf.get_rect(center=button_rect.center)
            self.screen.blit(text_surf, text_rect)

        footer = self.font_small.render("ESC - Wyjscie", True, LIGHT_GRAY)
        footer_rect = footer.get_rect(center=(center_x, 750))
        self.screen.blit(footer, footer_rect)

    def _draw_placement(self):
        # Plansze
        self.player.draw(self.screen, show_ships=True)
        self.ai.draw(self.screen, show_ships=False)

        # Panel rozmieszczania
        self.player.draw_placement_panel(self.screen)

        # Przeciagany statek
        mouse_pos = pygame.mouse.get_pos()
        self.player.draw_dragging_ship(self.screen, mouse_pos)

        # Komunikat
        if self.message and self.message_timer > 0:
            msg_bg = pygame.Rect(MESSAGE_X - MESSAGE_WIDTH // 2, MESSAGE_Y,
                                 MESSAGE_WIDTH, MESSAGE_HEIGHT)
            pygame.draw.rect(self.screen, DARK_BLUE, msg_bg, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, msg_bg, 2, border_radius=10)

            msg_text = self.font_medium.render(self.message, True, WHITE)
            msg_rect = msg_text.get_rect(center=msg_bg.center)
            self.screen.blit(msg_text, msg_rect)

        if not self.player.ready:
            ready_text = self.font_small.render("ENTER - Gotowy do gry", True, GREEN)
            ready_rect = ready_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

            bg_rect = ready_rect.inflate(40, 20)
            pygame.draw.rect(self.screen, DARK_BLUE, bg_rect, border_radius=8)
            pygame.draw.rect(self.screen, GREEN, bg_rect, 2, border_radius=8)
            self.screen.blit(ready_text, ready_rect)

    def _draw_battle(self):
        # Plansze
        self.player.draw(self.screen, show_ships=True)
        self.ai.draw(self.screen, show_ships=False)

        # Panel tury
        turn_bg = pygame.Rect(SCREEN_WIDTH // 2 - 200, 30, 400, 60)
        pygame.draw.rect(self.screen, DARK_BLUE, turn_bg, border_radius=10)
        pygame.draw.rect(self.screen, GOLD, turn_bg, 2, border_radius=10)

        if self.current_turn == "player":
            turn_text = self.font_medium.render("TWOJA TURA - STRZELAJ!", True, GREEN)
        else:
            turn_text = self.font_medium.render("TURA KOMPUTERA - CZEKAJ...", True, RED)

        turn_rect = turn_text.get_rect(center=turn_bg.center)
        self.screen.blit(turn_text, turn_rect)

        # Komunikat
        if self.message and self.message_timer > 0:
            msg_bg = pygame.Rect(MESSAGE_X - MESSAGE_WIDTH // 2, MESSAGE_Y + 80,
                                 MESSAGE_WIDTH, MESSAGE_HEIGHT)
            pygame.draw.rect(self.screen, DARK_BLUE, msg_bg, border_radius=10)
            pygame.draw.rect(self.screen, WHITE, msg_bg, 2, border_radius=10)

            msg_text = self.font_medium.render(self.message, True, WHITE)
            msg_rect = msg_text.get_rect(center=msg_bg.center)
            self.screen.blit(msg_text, msg_rect)

        # Paski statusu
        self._draw_ship_status()

        # Poziom trudnosci
        diff_text = self.font_small.render(f"Poziom: {DIFFICULTY_LEVELS[self.difficulty]}", True, WHITE)
        diff_rect = diff_text.get_rect(topright=(SCREEN_WIDTH - 50, 50))

        bg_rect = diff_rect.inflate(20, 10)
        bg_rect.x = SCREEN_WIDTH - bg_rect.width - 30
        pygame.draw.rect(self.screen, DARK_BLUE, bg_rect, border_radius=5)
        pygame.draw.rect(self.screen, WHITE, bg_rect, 1, border_radius=5)
        self.screen.blit(diff_text, diff_rect)

    def _draw_ship_status(self):
        y_pos = STATUS_BAR_Y_OFFSET

        # Status gracza
        player_sunk = sum(1 for ship in self.player.board.ships if ship.is_sunk())
        player_total = len(self.player.board.ships)

        self._draw_status_bar(self.screen,
                              BOARD_OFFSET_X, y_pos,
                              player_sunk, player_total,
                              "TWOJE STATKI", GREEN)

        # Status AI
        ai_sunk = sum(1 for ship in self.ai.board.ships if ship.is_sunk())
        ai_total = len(self.ai.board.ships)

        self._draw_status_bar(self.screen,
                              BOARD2_OFFSET_X, y_pos,
                              ai_sunk, ai_total,
                              "STATKI WROGA", RED)

    def _draw_status_bar(self, screen, x, y, sunk, total, label, color):
        # Tlo
        bg_rect = pygame.Rect(x, y, STATUS_BAR_WIDTH, STATUS_BAR_HEIGHT)
        pygame.draw.rect(screen, DARK_GRAY, bg_rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, bg_rect, 1, border_radius=5)

        # Wypelnienie
        if total > 0:
            health = 1 - (sunk / total)
            fill_rect = pygame.Rect(x + 2, y + 2,
                                    int((STATUS_BAR_WIDTH - 4) * health),
                                    STATUS_BAR_HEIGHT - 4)
            pygame.draw.rect(screen, color, fill_rect, border_radius=4)

        # Tekst
        text = self.font_small.render(f"{label}: {sunk}/{total}", True, WHITE)
        text_rect = text.get_rect(midleft=(x + 10, y + STATUS_BAR_HEIGHT // 2))
        screen.blit(text, text_rect)

    def _draw_game_over(self):
        # Przyciemnienie
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        self.screen.blit(s, (0, 0))

        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2

        # Panel
        panel_bg = pygame.Rect(center_x - 300, center_y - 150, 600, 300)
        pygame.draw.rect(self.screen, DARK_BLUE, panel_bg, border_radius=20)
        pygame.draw.rect(self.screen, GOLD, panel_bg, 3, border_radius=20)

        if self.winner == "GRACZ":
            result_text = "ZWYCIESTWO!"
            result_color = GREEN
            sub_text = "Gratulacje! Pokonales komputer!"
        else:
            result_text = "PORAZKA"
            result_color = RED
            sub_text = "Komputer okazal sie lepszy. Sprobuj ponownie!"

        # Tekst wyniku
        winner_text = self.font_large.render(result_text, True, result_color)
        winner_rect = winner_text.get_rect(center=(center_x, center_y - 80))
        self.screen.blit(winner_text, winner_rect)

        # Podtekst
        subtitle = self.font_medium.render(sub_text, True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(center_x, center_y))
        self.screen.blit(subtitle, subtitle_rect)

        # Statystyki
        if self.ai and self.ai.board:
            player_sunk = sum(1 for ship in self.ai.board.ships if ship.is_sunk())
        else:
            player_sunk = 0

        if self.player and self.player.board:
            ai_sunk = sum(1 for ship in self.player.board.ships if ship.is_sunk())
        else:
            ai_sunk = 0

        stats_text = self.font_small.render(
            f"Twoje trafienia: {player_sunk}/5   |   Trafienia komputera: {ai_sunk}/5",
            True, LIGHT_GRAY)
        stats_rect = stats_text.get_rect(center=(center_x, center_y + 50))
        self.screen.blit(stats_text, stats_rect)

        # Przycisk
        restart_btn = pygame.Rect(center_x - 150, center_y + 120, 300, 50)
        pygame.draw.rect(self.screen, DARK_GRAY, restart_btn, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, restart_btn, 2, border_radius=10)

        restart_text = self.font_medium.render("ESC - Menu glowne", True, WHITE)
        restart_rect = restart_text.get_rect(center=restart_btn.center)
        self.screen.blit(restart_text, restart_rect)

    def _handle_game_over_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = "MENU"
                self.player = None
                self.ai = None


if __name__ == "__main__":
    game = Game()
    game.run()