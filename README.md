# Gra-w-statki-Python
Opis projektu

Gra w statki napisana w języku Python z wykorzystaniem biblioteki Pygame. Projekt umożliwia rozgrywkę przeciwko komputerowi na trzech poziomach trudności. Celem gry jest zatopienie wszystkich statków przeciwnika poprzez strzelanie w pola na planszy.
Wymagania

Python 3.8 lub nowszy

Pygame 2.5.0 lub nowszy

Instalacja

Sprawdź czy Python jest zainstalowany:
    python --version

Zainstaluj bibliotekę Pygame:
    pip install pygame

Pobierz wszystkie pliki projektu do jednego folderu

Uruchomienie

W terminalu, w folderze z projektem wpisz:
    python main.py
lub
    python3 main.py
Struktura projektu

Projekt składa się z 7 plików:

main.py - plik uruchomieniowy
game.py - główna logika gry, stany, obsługa zdarzeń
constants.py - stałe, kolory, wymiary, ustawienia
board.py - klasa planszy, rysowanie siatki, obsługa strzałów
ship.py - klasa statku, rysowanie, trafienia, zatapianie
player.py - klasa gracza, rozmieszczanie statków, strzelanie
ai.py - sztuczna inteligencja, 3 poziomy trudności
Zasady gry
Rozmieszczanie statków

Gracz posiada 5 statków:

Lotniskowiec (4 pola)

Krążownik (3 pola)

Niszczyciel (2 pola)

Okręt podwodny (1 pole)

Okręt podwodny 2 (1 pole)

Statki nie mogą się stykać ze sobą ani wychodzić poza planszę.
Rozgrywka

Gracze na przemian strzelają w pola na planszy przeciwnika. Trafienie oznacza możliwość oddania kolejnego strzału. Pudło kończy turę. Gra kończy się gdy jeden z graczy zatopi wszystkie statki przeciwnika.

Menu główne:

1 - wybór poziomu łatwego
2 - wybór poziomu średniego
3 - wybór poziomu trudnego
ESC - wyjście z gry
Rozmieszczanie statków:

LPM (lewy przycisk myszy) - przeciąganie statku
PPM (prawy przycisk myszy) - zmiana orientacji (poziomo/pionowo)
SPACJA - automatyczne rozmieszczenie statków
R - resetowanie planszy
ENTER - potwierdzenie gotowości i rozpoczęcie gry
Bitwa:

LPM (lewy przycisk myszy) - strzał w pole na planszy przeciwnika
Poziomy trudności

Łatwy - komputer strzela w losowe, nieostrzelane wcześniej pola
Średni - komputer po trafieniu zapamiętuje sąsiednie pola i strzela w nie, dopóki nie zatopi statku
Trudny - komputer rozpoczyna od strzałów w co drugie pole, po trafieniu analizuje kierunek statku i kontynuuje wzdłuż linii
Interfejs:

Lewa plansza - statki gracza
Prawa plansza - statki komputera (ukryte)
Panel środkowy - lista statków do rozmieszczenia
Górny panel - komunikaty o turze i wynikach strzałów
Dolne paski - status zatopionych statków
Konfiguracja

W pliku constants.py można zmienić:

ROZMIAR PLANSZY
BOARD_SIZE = 10

ROZMIAR KOMÓRKI
CELL_SIZE = 40

POŁOŻENIE PLANESZ
BOARD_OFFSET_X = 100
BOARD_OFFSET_Y = 150
BOARD2_OFFSET_X = 950
BOARD2_OFFSET_Y = 150

KOLORY STATKÓW
SHIP_COLORS = {
4: (110, 50, 20),
3: (70, 70, 90),
2: (0, 90, 90),
1: (45, 25, 75)
}
Rozwiązywanie problemów

Błąd: pygame not found
Rozwiązanie: pip install pygame

Błąd: No module named 'constants'
Rozwiązanie: sprawdź czy plik constants.py znajduje się w tym samym folderze

Błąd: NameError: name 'random' is not defined
Rozwiązanie: w pliku game.py dodaj na górze import random
Autor:

Mikolaj Smoczynski
