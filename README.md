# 🧱 Voxel Editor
**Autor**: Helena Jońca\
**Technologie**: Python, OpenGL 3.3+, GLSL, GLFW, PyOpenGL, NumPy

## Spis treści
* [Opis projektu](#opis-projektu)
* [Struktura projektu](#struktura-projektu)
* [Instrukcja uruchomienia](#instrukcja-uruchomienia)
* [Technologie](#technologie)
* [Zrzuty ekranu](#zrzuty-ekranu)


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
├── Textures/                      
├── app.py                   # start aplikacji i główna pętla
├── camera.py                # ruch i macierze kamery.
├── constansts.py            # stałe projektu.
├── opengl_helpers.py        # funkcje pomocnicze OpenGL
├── requirements.txt
├── shaders.py               #definicje i kompilacja shaderów (vertex/fragment)
├── utils.py                 #funkcje pomocnicze
├── voxel_editor.py          #logika edytora: dodawanie, usuwanie voxelów, wybór materiału i interakcja z użytkownikiem.
```
## Instrukcja uruchomienia
1. Sklonuj repozytorium i przejdź do folderu
    ```bash
    https://github.com/ziraaell/VoxelEditor.git && cd VoxelEditor
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

## Technologie 
- PyOpenGL – obsługa OpenGL w Pythonie
- PyOpenGL_accelerate – przyspieszenie operacji OpenGL
- glfw – tworzenie okna, obsługa wejścia (mysz, klawiatura)
- numpy – operacje matematyczne na macierzach i wektorach
- Pillow (PIL) – wczytywanie obrazów
- time, math – standardowa biblioteka Pythona

Zbiór tekstur w folderze Textures/:
- [grass.jpg](https://stablediffusionweb.com/image/29289616-seamless-cartoon-grass-texture)
- [stone.jpg](https://pl.freepik.com/darmowe-wektory/tekstura-sciany-kamiennej_957408.htm)
- [wood.jpg](https://stablediffusionweb.com/image/20172220-cartoon-wood-texture-game-art)
- [sand.jpg](https://www.istockphoto.com/illustrations/background-of-beach-sand-texture-seamless)
- [leaves.jpg](https://kr.pinterest.com/pin/713187291026216994/)

## Zrzuty ekranu
1. Ekran startowy
   
<img width="1000" height="800" alt="image" src="https://github.com/user-attachments/assets/b1457687-0ed9-4097-81c4-44498496a926" />

2. Obracanie kamerą
   
![gif1](https://github.com/user-attachments/assets/6d2e7f37-ee32-4d4f-b95e-e26cbba0fe94)

3. Przybliżanie kamerą
   
![gif2](https://github.com/user-attachments/assets/c6b2979c-c553-456e-8c05-24f239e9b87c)

4. Usuwanie bloków
   
![gif3](https://github.com/user-attachments/assets/12f76214-1a48-446f-ac94-bd7a1b0cee3b)

5. Dodawanie bloków
    
![gif4](https://github.com/user-attachments/assets/e84185a8-1f36-4fb3-9cf3-6e17a43f6895)

6. Wybór tekstur
    
![gif5](https://github.com/user-attachments/assets/b71917a6-69c6-410a-bbba-8236cedfd570)
  

   
