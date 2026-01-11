"""
Pinky - różowy duszek

Tryby:
Chase - poscig, celuje w 4 pola przed pacmanem
Scatter - udaje sie do bezpiecznego rogu (lewy gorny)
Frightend - zmiana koloru i chaotyczne ruchy
Eaten - wraca do domku
"""

import pygame
import math
import CONST as const
from board import board as grid
from hero import CapMan as pacman

def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def convert(x, y):
    return (x+1)*const.TILE_SIZE_X, (y+1)*const.TILE_SIZE_Y

def undo(x, y):
    return (x//const.TILE_SIZE_X)-1, (y//const.TILE_SIZE_Y)-1

class Pinky(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.home_x, self.home_y = convert(22.5, 9)
        self.direction = const.LEFT
        self.mode = "SCATTER"
        self.speed = const.PINKY_SPEED
        self.angle = 0
        self.image = pygame.image.load("cap_man_1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(45,45))
        self.rect = self.image.get_rect(center = (self.home_x, self.home_y))
    def get_target(self, pacman):
        if self.mode == "SCATTER": return 0, 0
        if self.mode == "FRIGHTEND": return -1, -1
        if self.mode == "EATEN": return self.home_x, self.home_y
        target_x = pacman.rect.x + (4*pacman.capman_direction)
        target_y = pacman.rect.y + (4*pacman.capman_direction)
        return target_x, target_y
    def update(self, pacman):
        target_x, target_y = self.get_target(pacman)
        if self.mode == "CHASE" or self.mode == "SCATTER": self.speed = const.PINKY_SPEED
        elif self.mode == "FRIGHTEND": self.speed = const.FRIGHTENED_SPEED
        elif self.mode == "EATEN": self.speed = const.EATEN_SPEED
        #move towards the target based on manhattan distance
        #a: puste pole
        #b, m: ściany
        #n: mały pkt
        #o: duży pkt
        #p: ściana duszków
        dist = 2**32-1
        direction = None
        for i in range(4):
            candidate_x, candidate_y = undo(self.rect.x, self.rect.y)
            candidate_x, candidate_y = candidate_x+ const.DIRECTIONS[i][0], candidate_y + const.DIRECTIONS[i][1]
            if candidate_x < 0 or candidate_y < 0 or candidate_x >= len(grid) or candidate_y > len(grid[0]): continue
            if grid[candidate_x][candidate_y] in 'bm': continue
            if manhattan(candidate_x, candidate_y, target_x, target_y) < dist:
                direction = const.DIRECTIONS[i]
                dist = manhattan(candidate_x, candidate_y, target_x, target_y)
        if direction is not None:
            self.rect.x += direction[0] * self.speed
            self.rect.y += direction[1] * self.speed