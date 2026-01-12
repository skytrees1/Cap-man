import pygame as p
import math
import CONST as const
from board import board as grid
from hero import Capman as capman
from random import randint

'''
czerwony duszek
strateia - sledzi cap-mana
po aktualnych wspolzednych
'''

def manhattan(staring_x, starting_y, target_x, target_y):
    return abs(staring_x-target_x)+abs(starting_y-target_y)



class red(p.sprite.Sprite):
    def __init__(self):
        super().__init()
        self.direction=const.RIGHT
        self.home_x = 24.5*const.TILE_SIZE_X
        self.home_y = 9.5*const.TILE_SIZE_Y
        self.mode="SCATTER"
        self.speed = const.PINKY_SPEED
        self.angle=0
        self.image = p.image.load("cap_man_1.png").convert_alpha()
        self.image = p.transform.scale(self.image,(45,45))
        self.rect = self.image.get_rect(center = (self.home_x, self.home_y))
        self.cooldown = 0


    def mode_update(self, time):
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


    def choose_target_tile(self, capman):
        if self.mode=="SCATTER":
            return #prawy górny
        if self.mode=="EATEN":
            return self.home_x, self.home_y
        if self.mode=="FRIGHTENED":
            return -1, -1
        return capman.rect.centerx, capman.rect.centery
    
    def is_tile_possible(self, x, y):
        if x<0 or y>len(grid) or y<0 or x>len(grid[0]):
            return False
        if self.mode=="CHASE" and grid[y][x]=='p':
            return False
        if grid[y][x] in "bcdefghijklm":
            return False
        return True

    def choose_next_tile(self, capman):
        if self.rect.x % const.TILE_SIZE_X != 0: return
        if self.rect.y % const.TILE_SIZE_Y != 0: return
 
        target_x, target_y = self.choose_target_tile(capman)
        current_route = float('+inf')
        if self.mode=="FRIGHTENED":
            while(1):
                i = randint(0, 4)
                temp_x = self.rect.x + DIRECTIONS[i][0]
                temp_y = self.rect.y + DIRECTIONS[i][1]
                if self.is_tile_possible(temp_x, temp_y)==True:
                    return temp_x, temp_y
        for i in (0, 4):
            if self.direction[0]==DIRECTIONS[i][0] and self.direction[1]==DIRECTIONS[i][1]: continue
            if self.direction[0]==DIRECTIONS[i][0]*(-1) and self.direction[1]==DIRECTIONS[i][1]*(-1): continue
            temp_x = self.rect.x + DIRECTIONS[i][0]
            temp_y = self.rect.y + DIRECTIONS[i][1]
            if self.is_tile_possible(temp_x, temp_y)==False:
                continue
            temp_route = manhattan(temp_x, temp_y, target_x, target_y)
            if temp_route>current_route:
                current_route=temp_route
                next_x = temp_x
                next_y = temp_y
        return next_x, next_y
    
    def update(self, capman, time):
        self.mode_update(time)

        if self.rect.x % const.TILE_SIZE_X != 0 and self.rect.y % const.TILE_SIZE_Y != 0:
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed
            return
        
        target_x, target_y = self.choose_target_tile(capman)

        if self.mode=="CHASE" or self.mode=="SCATTER":
            self.speed=const.PINKY_SPEED
        if self.mode=="FRIGHTENED":
            self.speed = const.FRIGHTENED_SPEED
        if self.mode=="EATEN":
            self.speed=const.EATEN_SPEED

        next_x, next_y = self.choose_next_tile
        direction=[2]
        direction[0]=self.rect.x-next_x
        direction[1]=self.rect.y-next_y
        self.rect.x += direction[0]*self.speed
        self.rect.y +=direction[1]*self.speed

        if self.mode == "EATEN" and abs(self.rect.x - self.home_x) < 2 and abs(self.rect.y - self.home_y) < 2: 
            self.mode == "SCATTER"
            self.cooldown = 5 



