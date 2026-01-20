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

#odleglosc miedzy punktami w metryce miejskiej
def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

class Pinky(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #wspolrzedne poczatkowe
        self.home_x, self.home_y = 23.5*const.TILE_SIZE_X, 9.5*const.TILE_SIZE_Y
        #kierunek poczatkowy
        self.direction = const.LEFT
        #tryb poczatkowy
        self.mode = "SCATTER"
        #predkosc domyslna
        self.speed = const.PINKY_SPEED
        #obrazek
        self.angle = 0
        self.image = pygame.image.load("cap_man_1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(45,45))
        #miejsce poczatkowe
        self.rect = self.image.get_rect(center = (self.home_x, self.home_y))
        #cooldown po zjedzeniu
        self.cooldown = 0
    def get_target(self, pacman):
        #jezeli scatter to idzie do gornego rogu
        if self.mode == "SCATTER": return 0, 0
        #jezeli frightend to losowy ruch
        if self.mode == "FRIGHTEND": return -1, -1
        #jezeli eaten to wraca do domu
        if self.mode == "EATEN": return self.home_x, self.home_y
        #jezeli chase to mierzy 4 kratki przed pacmanem
        target_x = pacman.rect.centerx# // const.TILE_SIZE_X #+ (4*pacman.capman_direction)
        target_y = pacman.rect.centery# // const.TILE_SIZE_Y #+ (4*pacman.capman_direction)
        return target_x, target_y
    def mode_update(self, time):
        #zmiena trybu wzgledem czasu trwania rozgrywki
        if self.mode == "FRIGHTEND": return
        if self.mode == "EATEN": return
        if 0 < time <= 7: self.mode = "SCATTER"
        elif 7 < time <= 27: self.mode = "CHASE"
        elif 27 < time <= 34: self.mode = "SCATTER"
        elif 34 < time <= 54: self.mode = "CHASE" 
        elif 54 < time <= 59: self.mode = "SCATTER"
        elif 59 < time <= 79: self.mode = "CHASE"
        elif 79 < time <= 84: self.mode = "SCATTER"
        else: self.mode = "CHASE"
    def possible(self, y, x):
        #sprawdza mozliwosc wejscia na dane pole
        if 0 <= y < len(grid):
            x = x % len(grid[0])
            if self.mode == "CHASE" and grid[y][x] == 'p': return False
            if grid[y][x] in 'bcdefghijklm': return False
            return True
        return False
    
    def update(self, pacman, time):
        #wykonanie ruchu
        #aktualizacja trybu
        self.mode_update(time)
        
        #jezeli nie jestesmy w srodku kafelka to nie zmieniamy kieruku
        #ruch w taka strone jak poprzedni
        if self.rect.x % const.TILE_SIZE_X != 0 and self.rect.y % const.TILE_SIZE_Y != 0:
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed
            return
        
        #zmieniamy kierunek wzgledem dystanstu w metryce miejskiej
        target_x, target_y = self.get_target(pacman)
        
        #zmiana predkosci w zaleznosci od trybu
        if self.mode == "CHASE" or self.mode == "SCATTER": self.speed = const.PINKY_SPEED
        elif self.mode == "FRIGHTEND": self.speed = const.FRIGHTENED_SPEED
        elif self.mode == "EATEN": self.speed = const.EATEN_SPEED
        
        #szukanie kafelka ktory nas przybilzy do celu
        dist = 2**32-1
        direction = None
        half_tile_size = const.TILE_SIZE_X//2
        tile_x = self.rect.centerx // const.TILE_SIZE_X
        tile_y = self.rect.centery // const.TILE_SIZE_Y
        
        for i in range(4):
            #zapobiegamy naglej zmianie kierunku poza "skrzyzowaniem"
            if (self.direction == const.LEFT and const.DIRECTIONS[i] == const.RIGHT): continue
            if (self.direction == const.RIGHT and const.DIRECTIONS[i] == const.LEFT): continue
            if (self.direction == const.UP and const.DIRECTIONS[i] == const.DOWN): continue
            if (self.direction == const.DOWN and const.DIRECTIONS[i] == const.UP): continue
            
            new_x = (self.rect.centerx + const.DIRECTIONS[i][0] * half_tile_size)# / const.TILE_SIZE_X
            new_y = (self.rect.centery + const.DIRECTIONS[i][1] * half_tile_size)# / const.TILE_SIZE_Y
            
            if not self.possible(new_y // const.TILE_SIZE_Y, new_x // const.TILE_SIZE_Y): continue
            
            if manhattan(new_x, new_y, target_x, target_y) < dist:
                direction = const.DIRECTIONS[i]
                dist = manhattan(new_x, new_y, target_x, target_y)

        if direction is None: direction = self.direction
        if direction is not None:
            self.direction = direction
            self.rect.x += direction[0] * self.speed
            self.rect.y += direction[1] * self.speed
        
        #jezeli eaten i w domu to zmaina na scatter
        if self.mode == "EATEN" and abs(self.rect.x - self.home_x) < 2 and abs(self.rect.y - self.home_y) < 2: 
            self.mode == "SCATTER"
            self.cooldown = 5 

    def collision(self, pacman):
        pinky_tile_x = self.rect.centerx // const.TILE_SIZE_X
        pinky_tile_y = self.rect.centery // const.TILE_SIZE_Y

        pacman_tile_x = pacman.rect.centerx // const.TILE_SIZE_X
        pacman_tile_y = pacman.rect.centery // const.TILE_SIZE_Y

        return ((pinky_tile_x == pacman_tile_x) and (pinky_tile_y == pacman_tile_y))