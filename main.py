#!/usr/bin/env python3
"""
BATTLESHIP - Gra w Statki
Pojedynek z komputerem
"""

import pygame
from game import Game


def main():
    print("=" * 50)
    print("                    BATTLESHIP")
    print("                    Gra w Statki")
    print("=" * 50)
    print("\nWitaj w grze! Wybierz poziom trudnosci.")
    print("1 - Latwy | 2 - Sredni | 3 - Trudny\n")

    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Blad: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        print("\nDziekujemy za gre!")


if __name__ == "__main__":
    main()