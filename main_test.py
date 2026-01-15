"""
Program do testu
"""


import pygame as p
import copy
from board import board
from CONST import *
from map_generator import draw_map
from hero import CapMan

p.init()

# ekrany 
screen = p.display.set_mode((WIDTH, HEIGHT), p.RESIZABLE)
game_screen = p.Surface((WIDTH, HEIGHT))

clock = p.time.Clock()

# obiekty
player = p.sprite.GroupSingle()
player.add(CapMan())

level = copy.deepcopy(board)

# Zmienne do obsługi punktacji
score = 0
game_font = p.font.SysFont("arial", 30) 

def check_point_collision(player_sprite, current_level, current_score):
    # Obliczamy indeksy kafelka, na którym znajduje się środek gracza
    tile_x = player_sprite.rect.centerx // TILE_SIZE_X
    tile_y = player_sprite.rect.centery // TILE_SIZE_Y

    # Zabezpieczenie przed wyjściem poza zakres tablicy
    if 0 <= tile_y < len(current_level) and 0 <= tile_x < len(current_level[0]):
        tile_content = current_level[tile_y][tile_x]

        if tile_content == 'n':      # Mały punkt
            current_level[tile_y][tile_x] = 'a' # Zamień na puste pole ('a')
            return current_score + 10
        elif tile_content == 'o':    # Duży punkt
            current_level[tile_y][tile_x] = 'a' # Zamień na puste pole ('a')
            return current_score + 50
            
    return current_score

running = True

# pętla główna 

while running:

    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

        elif event.type == p.KEYDOWN:
            last_key = player.sprite.checking_Pressed_Keys()
            if last_key != None:
                player.sprite.capman_direction = last_key
                player.sprite.player_rotation(player.sprite.capman_direction)

        elif event.type == p.VIDEORESIZE:
            # Aktualizujemy prawdziwy ekran do nowych wymiarów
            width, height = event.w, event.h
            screen = p.display.set_mode((width, height), p.RESIZABLE)

    game_screen.fill('black')
    draw_map(game_screen, level)
    player.draw(game_screen)
    player.update(player.sprite.capman_direction)

    #Sprawdzenie kolizji z punktami i aktualizacja wyniku
    score = check_point_collision(player.sprite, level, score)
    score_text = game_font.render(f"Licznik punktów: {score}", True, "white")
    game_screen.blit(score_text, (50, HEIGHT - 50))

    # skalowanie obrazu 
    current_w, current_h = screen.get_size()
    scaled_surface = p.transform.smoothscale(game_screen, (current_w, current_h))
    screen.blit(scaled_surface, (0, 0))

    p.display.flip()
    clock.tick(60)
p.quit()
