# 🧱 Voxel Editor
**Autor**: Helena Jońca\
**Technologie**: Python, OpenGL 3.3+, GLSL, GLFW, PyOpenGL, NumPy

## Spis treści
* [Opis projektu](#opis-projektu)
* [Instrukcja obsługi](#instrukcja_obsluga)
* [Sttruktura projektu](#project-structure)
* [Technologie](#setup)
* [Screenshots](#screenshots)


## Opis projektu
**Voxel Editor** to interaktywna aplikacja 3D umożliwiająca tworzenie i edycję scen w oparciu o voxele (sześcienne elementy przestrzeni). Program renderuje sześciany z teksturami, obsługuje oświetlenie Phonga oraz umożliwia użytkownikowi pełną nawigację kamerą oraz interakcję z obiektami.

Aplikacja wykorzystuje:
- projekcję perspektywiczną i macierz kamery (perspective, look_at),
- geometrię sześcianu (pozycje, UV, normalne),
- system podświetlania zaznaczonego bloku,
- tekstury i materiały,
- vertex oraz fragment shadery w GLSL.

## Struktura projektu
```
Car-Rental-Databases-Project/          
├── README.md                
├── app.py                   # Główna aplikacja
```
## Instrukcja uruchomienia
    1. Sklonuj repozytorium i przejdź do folderu
    ```bash

    ```

    2.  Utworzenie środowiska
    ```bash
        python -m venv venv
    ```

    3. Aktywacja środowiska
        - Windows
        ```bash
            venv\Scripts\activate
        ```

        - Linux/macOS
        ```bash
            source venv/bin/activate
        ```
    4. Instalacja zależności
    ```bash
        python -m pip install --upgrade pip
        python -m pip install -r requirements.txt
    ```

    5. Uruchomienie programu
    ```bash
        python app.py
    ```

3. Project structure