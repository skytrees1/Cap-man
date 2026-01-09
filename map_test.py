"""
Program do testu mapy, capmana
"""


import pygame as p
import copy
from board import board
from CONST import *
from map_generator import draw_map
from hero import CapMan

p.init()

screen = p.display.set_mode((WIDTH, HEIGHT))
clock = p.time.Clock()

player = p.sprite.GroupSingle()
player.add(CapMan())

level = copy.deepcopy(board)

running = True

while running:

    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        if event.type == p.KEYDOWN:
            last_key = player.sprite.checking_Pressed_Keys()
            if last_key != None:
                player.sprite.capman_direction = last_key
                player.sprite.player_rotation(player.sprite.capman_direction)
    screen.fill('black')
    draw_map(screen, level)
    player.draw(screen)
    player.update(player.sprite.capman_direction)
    p.display.flip()
    clock.tick(60)
p.quit()
