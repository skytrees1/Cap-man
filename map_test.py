"""
Program do testu mapy, capmana
"""


import pygame as p
import copy
from board import board
from CONST import *
from map_generator import draw_map
from hero import CapMan
from pinky import Pinky
from clyde import Clyde
from red import red
from inky import inky

p.init()

screen = p.display.set_mode((WIDTH, HEIGHT))
clock = p.time.Clock()

start_time = p.time.get_ticks() #czas dla duszkow

player = p.sprite.GroupSingle()
player.add(CapMan())

pinky = p.sprite.GroupSingle()
pinky.add(Pinky())

clyde = p.sprite.GroupSingle()
clyde.add(Clyde())

ghost_red = p.sprite.GroupSingle()
ghost_red.add(red())

ghost_inky = p.sprite.GroupSingle()
ghost_inky.add(inky())

level = copy.deepcopy(board)

# Zmienne do obsługi punktacji
score = 0
game_font = p.font.SysFont("arial", 30) 
game_over_font = p.font.SysFont("arial", 60)
lives = 3

def reset_positions():
    global start_time
    start_time = p.time.get_ticks()

    player.empty()
    pinky.empty()
    clyde.empty()
    ghost_red.empty()
    ghost_inky.empty()

    player.add(CapMan())
    pinky.add(Pinky())
    clyde.add(Clyde())
    ghost_red.add(red())
    ghost_inky.add(inky())

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

def show_game_final_score():
    overlay = p.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180) # Przezroczystość (0-255)
    overlay.fill((0,0,0))
    screen.blit(overlay, (0,0))
    
    text_surf = game_over_font.render("GAME OVER", True, "red")
    score_surf = game_font.render(f"Wynik końcowy: {score}", True, "white")
    
    # Centrowanie napisów
    text_rect = text_surf.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
    score_rect = score_surf.get_rect(center=(WIDTH/2, HEIGHT/2 + 20))
    
    screen.blit(text_surf, text_rect)
    screen.blit(score_surf, score_rect)
    p.display.flip()
    
    # Zamrożenie gry na 3 sekundy
    p.time.delay(3000)

reset_positions()
running = True

while running:

    current_time_seconds = (p.time.get_ticks() - start_time) / 1000
    
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        if event.type == p.KEYDOWN:
            if event.key == p.K_ESCAPE:
                running = False
                exit()

            last_key = player.sprite.checking_Pressed_Keys()
            if last_key != None:
                player.sprite.direction = last_key
                player.sprite.player_rotation(player.sprite.direction)

    pinky.update(player.sprite, current_time_seconds)
    clyde.update(player.sprite, current_time_seconds)
    ghost_red.update(player.sprite, current_time_seconds)
    ghost_inky.update(player.sprite, ghost_red.sprite, current_time_seconds)

    player.update(player.sprite.direction)

    if (pinky.sprite.collision(player.sprite)or 
            clyde.sprite.collision(player.sprite)or
            ghost_red.sprite.collision(player.sprite)or
            ghost_inky.sprite.collision(player.sprite)):

            lives -= 1
            print(f"HP DOWN\nREAMANING: {lives}")
            player.draw(screen)
            p.display.flip()
            if lives > 0:
                p.time.delay(1000)
                reset_positions()
            else:
                show_game_final_score()
                running = False

    screen.fill('black')
    draw_map(screen, level)
    
    player.draw(screen)
    pinky.draw(screen)
    clyde.draw(screen)
    ghost_red.draw(screen)
    ghost_inky.draw(screen)

    #Sprawdzenie kolizji z punktami i aktualizacja wyniku
    score = check_point_collision(player.sprite, level, score)
    score_text = game_font.render(f"Licznik punktów: {score}", True, "white")
    screen.blit(score_text, (50, HEIGHT - 40))

    lives_text = game_font.render(f"Życia: {lives}", True, "red")
    screen.blit(lives_text, (WIDTH - 150, HEIGHT - 40))

    

    p.display.flip()
    clock.tick(60)
p.quit()
