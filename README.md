# CapMan
> Gra inspirowana kultowym Pac-Manem, wykonana przy użyciu języka Python oraz biblioteki Pygame.
---
## Spis treści 
* [O projekcie](#o-projekcie)
* [Cechy projektu](#cechy-projektu)
* [Sterowanie](#sterowanie)
* [Grafika z gry](#grafika-z-gry)
* [Uruchamianie programu](#uruchamianie-programu)
* [Twórcy](#twórcy)
---
## O projekcie
**CapMan** to gra zręcznościowa przygotowana w ramach zajęć z **Podstawowego Warsztatu Informatyka** na kierunku Informatyka (Wydział Matematyki i Informatyki Uniwersytetu Wrocławskiego).

Gra jest naszą interpretacją kultowego **Pac-Mana** z 1980 roku. Celem rozgrywki jest zebranie wszystkich punktów na mapie przy jednoczesnym unikaniu duchów. Tym, co odróżnia naszą wersję od oryginału, jest warstwa wizualna – unikalna czapeczka bohatera.

---
## Cechy projektu 
* **Architektura Obiektowa:** Kod zorganizowany w klasy dla zwiększenia czytelności i łatwej rozbudowy.
* **Reprezentacja Mapy:** Układ poziomu rysowany automatycznie na podstawie tablicy w kodzie.
* **Mechanika Gry:** Precyzyjne wykrywanie kolizji i płynny ruch postaci.
* **AI Przeciwników:** Duchy posiadają zaimplementowane różne algorytmy poruszania się po labiryncie.
* **Interfejs:** Menu główne, licznik punktów oraz możliwość swobodnego zmieniania rozmiaru okna gry.

---
## Sterowanie
Gra obsługiwana jest za pomocą klawiatury:
* **Strzałki / WASD** – poruszanie się postacią
* **ESC** - wyjście z gry

---
## Grafika z gry
tu będzie zdjęcie z gry

---
## Uruchamianie programu
Projekt został przetestowany na systemach **macOS** oraz **Windows 11** i są to zalecane systemy do uruchomienia gry. Niezbędny jest interpreter Python (wersja 3.6 lub nowsza ([Pobierz tutaj](https://www.python.org/downloads/))) oraz biblioteka Pygame (wersja 2.0 lub nowsza).

Aby rozpocząć rozgrywkę, należy uruchomić plik `main.py` za pomocą interpretera Python.

### Instrukcja instalcji bibliotek
* Windows
    ```bash
    python -m pip install -r requirements.txt
    ```
* Linux/macOS
    ```bash 
    python3 -m pip install -r requirements.txt
    ```
---
## Twórcy
Autorami projektu są:
* Maciej Jerzycki
* Maksym Kotulskyi
* Maja Kruszewska
* Mateusz Mucha
* Krzysztof Nowak
* Piotr Porzycki 
