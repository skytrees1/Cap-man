import pygame as p
import copy
from board import board
from CONST import *
from map_generator import draw_map
from hero import CapMan

p.init()

screen = p.display.set_mode((WIDTH, HEIGHT))
clock = p.time.Clock()
running = True

player = p.sprite.GroupSingle()
player.add(CapMan())

while running:

    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        if event.type == p.KEYDOWN:
            last_key = player.sprite.checking_Pressed_Keys()
            if last_key != None:
                PRESSED_KEY = last_key
                player.sprite.player_rotation(PRESSED_KEY)
    screen.fill('black')
    draw_map(screen)
    player.draw(screen)
    player.update(PRESSED_KEY)
    p.display.flip()
    clock.tick(60)
p.quit()
