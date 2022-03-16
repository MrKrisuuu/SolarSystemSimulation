from Visualizer import *
from SolarSystem import *


if __name__ == "__main__":
    INSTRUCTION = """
Program pokazuje aktualne pozycje planet w Układzie Słonecznym i oblicza następne położenia planet.
Umożliwia następujące opcje:
- przesuwanie symulacji klikając i odpowiednio przesuwając po planszy symulacji (czarny kwadrat)
- oddalanie i przybliżanie za pomocą środkowego przycisku myszy
- zatrzymanie symulacji przyciskiem "STOP"
- ustawianie prędkości symulacji za pomocą suwaka
- dodanie obiektu po naciśnięciu przycisku "ADD" i wpisaniu odpowiedniej masy (w masach Słońca), a następnie klikając gdziekolwiek na planszy
- usunięcie z symulacji obiektu za pomocą przycisku "REMOVE"
- jeżeli się rozmyślimy możemy anulować akcję przyciskiem "CANCEL"
    
Napisany przez Krzysztofa Surówkę, studenta 2 roku informatyki, jako projekt z Pythona.
30.06.2021
"""
    print(INSTRUCTION)
    space = create_solar_system()
    init_animation(space)
