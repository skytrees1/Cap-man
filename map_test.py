"""
Program do testu mapy
"""


import pygame as p
import copy
from board import board
from CONST import *
from map_generator import draw_map

p.init()

screen = p.display.set_mode((WIDTH, HEIGHT))
level = copy.deepcopy(board)
running = True
while running:

    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    screen.fill('black')
    draw_map(screen, level)
    p.display.flip()
p.quit()
