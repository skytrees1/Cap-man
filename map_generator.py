import pygame as p
from board import board
from CONST import *
import math
import copy

p.init()

level = copy.deepcopy(board)
# Funkcja rysująca poszczególne kafelki na mapie

def draw_map(screen, level):
    for i in range(len(level)):
        for j in range(len(level[i])):
            # pozioma linia niebieska
            if level[i][j] == "b":
                p.draw.line(screen, 'blue', (j * TILE_SIZE_X, i * TILE_SIZE_Y + (TILE_SIZE_Y / 2)), ((j + 1) * TILE_SIZE_X, i * TILE_SIZE_Y + (TILE_SIZE_Y / 2)), 3)
            # pionowa linia niebieska
            elif level[i][j] == "c":
                p.draw.line(screen, 'blue', (j * TILE_SIZE_X + (TILE_SIZE_X / 2), i * TILE_SIZE_Y), (j * TILE_SIZE_X + (TILE_SIZE_X / 2), (i + 1) * TILE_SIZE_Y), 3)
            # łuki niebieskie
            elif level[i][j] == "d":
                p.draw.arc(screen, 'blue', (j * TILE_SIZE_X  + (TILE_SIZE_X / 2) - 2, i * TILE_SIZE_Y + (TILE_SIZE_Y / 2) - 2, TILE_SIZE_X + 6, TILE_SIZE_Y +  6), math.pi / 2,  math.pi, 3)
            elif level[i][j] == "e":
                p.draw.arc(screen, 'blue', (j * TILE_SIZE_X  + (TILE_SIZE_X / 2) - 2, i * TILE_SIZE_Y - (TILE_SIZE_Y / 2) - 4, TILE_SIZE_X + 6, TILE_SIZE_Y + 6), math.pi,  math.pi * 3 /  2, 3)
            elif level[i][j] == "f":
                p.draw.arc(screen, 'blue', (j * TILE_SIZE_X  - (TILE_SIZE_X / 2) - 4, i * TILE_SIZE_Y + (TILE_SIZE_Y / 2) - 2, TILE_SIZE_X + 6, TILE_SIZE_Y +  6), 0,  math.pi / 2, 3)
            elif level[i][j] == "g":
                p.draw.arc(screen, 'blue', (j * TILE_SIZE_X  - (TILE_SIZE_X / 2) - 4, i * TILE_SIZE_Y - (TILE_SIZE_Y / 2) - 4, TILE_SIZE_X + 6, TILE_SIZE_Y +  6), math.pi * 3 / 2, 0, 3)
            # pozioma linia zielona
            elif level[i][j] == "h":
                p.draw.line(screen, 'green', (j * TILE_SIZE_X, i * TILE_SIZE_Y + (TILE_SIZE_Y / 2)), ((j + 1) * TILE_SIZE_X, i * TILE_SIZE_Y + (TILE_SIZE_Y / 2)), 3)
            # pionowa linia zielona
            elif level[i][j] == "i":
                p.draw.line(screen, 'green', (j * TILE_SIZE_X + (TILE_SIZE_X / 2), i * TILE_SIZE_Y), (j * TILE_SIZE_X + (TILE_SIZE_X / 2), (i + 1) * TILE_SIZE_Y), 3)
            # łuki zielone
            elif level[i][j] == "j":
                p.draw.arc(screen, 'green', (j * TILE_SIZE_X  + (TILE_SIZE_X / 2) - 2, i * TILE_SIZE_Y + (TILE_SIZE_Y / 2) - 2, TILE_SIZE_X + 6, TILE_SIZE_Y +  6), math.pi / 2,  math.pi, 3)
            elif level[i][j] == "k":
                p.draw.arc(screen, 'green', (j * TILE_SIZE_X  + (TILE_SIZE_X / 2) - 2, i * TILE_SIZE_Y - (TILE_SIZE_Y / 2) - 4, TILE_SIZE_X + 6, TILE_SIZE_Y + 6), math.pi,  math.pi * 3 /  2, 3)
            elif level[i][j] == "l":
                p.draw.arc(screen, 'green', (j * TILE_SIZE_X  - (TILE_SIZE_X / 2) - 4, i * TILE_SIZE_Y + (TILE_SIZE_Y / 2) - 2, TILE_SIZE_X + 6, TILE_SIZE_Y +  6), 0,  math.pi / 2, 3)
            elif level[i][j] == "m":
                p.draw.arc(screen, 'green', (j * TILE_SIZE_X  - (TILE_SIZE_X / 2) - 4, i * TILE_SIZE_Y - (TILE_SIZE_Y / 2) - 4, TILE_SIZE_X + 6, TILE_SIZE_Y +  6), math.pi * 3 / 2, 0, 3)
            # mała kropka
            elif level[i][j] == "n":
                p.draw.circle(screen, 'white', (j * TILE_SIZE_X + TILE_SIZE_X / 2, i * TILE_SIZE_Y + TILE_SIZE_Y / 2), 3)
            # większa kropka
            elif level[i][j] == "o":
                p.draw.circle(screen, 'yellow', (j * TILE_SIZE_X + TILE_SIZE_X / 2, i * TILE_SIZE_Y + TILE_SIZE_Y / 2), 7)
            # linia duchów
            elif level[i][j] == "p":
                p.draw.line(screen, 'white', (j * TILE_SIZE_X - (TILE_SIZE_X / 2) + 2, i * TILE_SIZE_Y + (TILE_SIZE_Y / 2)), ((j + 1) * TILE_SIZE_X + (TILE_SIZE_X / 2), i * TILE_SIZE_Y + (TILE_SIZE_Y / 2)), 3)
            
            


