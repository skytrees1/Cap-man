import pygame as p
import math
import CONST as const
from board import board as grid
import random
from collections import deque

def bfs(start_x, start_y, target_x, target_y, allowed):
    start_x, start_y = int(start_x), int(start_y)
    target_x, target_y = int(target_x), int(target_y)

    target_y = max(0, min(target_y, len(grid) - 1))
    target_x = max(0, min(target_x, len(grid[0]) - 1))

    if grid[target_y][target_x] not in allowed:
        return None

    queue = deque([(start_x, start_y, [(start_x, start_y)])])
    visited = {(start_x, start_y)}
    
    while queue:
        curr_x, curr_y, path = queue.popleft()
        if curr_x == target_x and curr_y == target_y: 
            return path[1] if len(path) > 1 else path[0]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = curr_x + dx, curr_y + dy
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                if (nx, ny) not in visited and grid[ny][nx] in allowed:
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + [(nx, ny)]))
    return None

class red(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.home_tile_x = 23
        self.home_tile_y = 9
        
        self.direction = const.UP
        self.next_direction = const.UP
        self.mode = "SCATTER"
        self.speed = const.PINKY_SPEED
        self.image = p.image.load('images/blinky/blinky_down_1.png').convert_alpha()
        self.image = p.transform.scale(self.image, (45, 45))
        
        start_px_x = self.home_tile_x * const.TILE_SIZE_X + const.TILE_SIZE_X // 2
        start_px_y = self.home_tile_y * const.TILE_SIZE_Y + const.TILE_SIZE_Y // 2
        self.rect = self.image.get_rect(center=(start_px_x, start_px_y))
        
        self.last_tile = (-1, -1)

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
        if self.mode=="FRIGHTENED": return -1, -1
        if self.mode == "SCATTER": return 38, 2
        if self.mode == "EATEN": return self.home_tile_x, self.home_tile_y
        return int(capman.rect.centerx // const.TILE_SIZE_X), int(capman.rect.centery // const.TILE_SIZE_Y)

    def frighten(self):
        #funkcja do wywolania w przypadku zjedzenia
        #przez capmana duzego punkta
        self.mode="FRIGHTENED"
        self.speed=const.FRIGHTENED_SPEED

    def update(self, capman, time):
        #do wywolywania co obrot petli
        if capman is None: return
        self.mode_update(time)
        if self.mode=="EATEN" and self.rect.centerx//const.TILE_SIZE_X==self.home_tile_x and self.rect.centery//const.TILE_SIZE_Y==self.home_tile_y:
            self.mode = "SCATTER"
            self.speed=const.PINKY_SPEED
        if self.mode == "EATEN": self.speed = const.EATEN_SPEED
        elif self.mode == "FRIGHTENED": self.speed = const.FRIGHTENED_SPEED
        else: self.speed = const.PINKY_SPEED

        curr_tile_x = int(self.rect.centerx // const.TILE_SIZE_X)
        curr_tile_y = int(self.rect.centery // const.TILE_SIZE_Y)
        center_x = curr_tile_x * const.TILE_SIZE_X + const.TILE_SIZE_X // 2
        center_y = curr_tile_y * const.TILE_SIZE_Y + const.TILE_SIZE_Y // 2

        allowed = "anop" if self.mode in ["SCATTER", "EATEN"] else "ano"

        if (curr_tile_x, curr_tile_y) != self.last_tile:
            
            if self.mode == "FRIGHTENED":
                possible_dirs = []
                for d in [const.UP, const.DOWN, const.LEFT, const.RIGHT]:
                    if d == (-self.direction[0], -self.direction[1]): 
                        continue
                    
                    nx, ny = curr_tile_x + d[0], curr_tile_y + d[1]
                    if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] in allowed:
                        possible_dirs.append(d)
                
                if possible_dirs:
                    self.next_direction = random.choice(possible_dirs)
                else:
                    self.next_direction = (-self.direction[0], -self.direction[1])

            else:
                target_x, target_y = self.choose_target_tile(capman)
                res = bfs(curr_tile_x, curr_tile_y, target_x, target_y, allowed) 
                
                if res:
                    nx, ny = res
                    if nx > curr_tile_x: self.next_direction = const.RIGHT
                    elif nx < curr_tile_x: self.next_direction = const.LEFT
                    elif ny > curr_tile_y: self.next_direction = const.DOWN
                    elif ny < curr_tile_y: self.next_direction = const.UP
            
            self.last_tile = (curr_tile_x, curr_tile_y)

        if self.direction != self.next_direction:
            if abs(self.rect.centerx - center_x) < self.speed and abs(self.rect.centery - center_y) < self.speed:
                self.rect.center = (center_x, center_y)
                self.direction = self.next_direction

        check_dist = 15 
        check_x = int((self.rect.centerx + self.direction[0] * check_dist) // const.TILE_SIZE_X)
        check_y = int((self.rect.centery + self.direction[1] * check_dist) // const.TILE_SIZE_Y)
        
        if 0 <= check_y < len(grid) and 0 <= check_x < len(grid[0]) and grid[check_y][check_x] in allowed:
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed
        else:
            self.last_tile = (-1, -1)
        
    def collision(self, capman):
        #do wywolania w przypadku kolizji reda z capmanem
        if self.mode == "EATEN": return False
        if self.mode == "FRIGHTENED":
            self.mode="EATEN"
            self.speed=const.EATEN_SPEED
        return self.rect.colliderect(capman.rect)