import pygame as p
import math
import CONST as const
from board import board as grid
import random
from collections import deque

def bfs(start_x, start_y, target_x, target_y, allowed, current_dir):
    start_x, start_y = int(start_x), int(start_y)
    target_x, target_y = int(target_x), int(target_y)

    target_y = max(0, min(target_y, len(grid) - 1))
    target_x = max(0, min(target_x, len(grid[0]) - 1))

    if grid[target_y][target_x] not in allowed:
        return None

    opposite_dir = (-current_dir[0], -current_dir[1])

    queue = deque([(start_x, start_y, [(start_x, start_y)])])
    visited = {(start_x, start_y)}
    
    while queue:
        curr_x, curr_y, path = queue.popleft()
        if curr_x == target_x and curr_y == target_y: 
            return path[1] if len(path) > 1 else path[0]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if len(path) == 1 and (dx, dy) == opposite_dir:
                continue

            nx, ny = curr_x + dx, curr_y + dy
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                if (nx, ny) not in visited and grid[ny][nx] in allowed:
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + [(nx, ny)]))
    return None

class inky(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.home_tile_x = 23
        self.home_tile_y = 8
        
        self.direction = const.UP
        self.next_direction = const.UP
        self.mode = "SCATTER"
        self.speed = const.PINKY_SPEED
        
        self.image = p.image.load('assets/images/inky/inky_down_1.png').convert_alpha()
        self.image = p.transform.scale(self.image, (45, 45))
        
        start_px_x = self.home_tile_x * const.TILE_SIZE_X + const.TILE_SIZE_X // 2
        start_px_y = self.home_tile_y * const.TILE_SIZE_Y + const.TILE_SIZE_Y // 2
        self.rect = self.image.get_rect(center=(start_px_x, start_px_y))
        
        self.last_tile = (-1, -1)

    def mode_update(self, time):
        if self.mode in ["FRIGHTENED", "EATEN"]: return
        if (0 < time <= 7) or (27 < time <= 34) or (54 < time <= 59) or (79 < time <= 84):
            self.mode = "SCATTER"
        else:
            self.mode = "CHASE"

    def choose_target_tile(self, capman, red_ghost):
        curr_tile_x = int(self.rect.centerx // const.TILE_SIZE_X)
        curr_tile_y = int(self.rect.centery // const.TILE_SIZE_Y)
        
        if grid[curr_tile_y][curr_tile_x] == 'p' or curr_tile_y >= 7:
            return 23, 5

        if self.mode == "SCATTER": 
            return len(grid[0]) - 3, len(grid) - 3
       
        
        if self.mode == "EATEN": 
            return self.home_tile_x, self.home_tile_y

        cap_dir = const.LEFT
        if capman.capman_direction == "move_right": cap_dir = const.RIGHT
        elif capman.capman_direction == "move_left": cap_dir = const.LEFT
        elif capman.capman_direction == "move_up": cap_dir = const.UP
        elif capman.capman_direction == "move_down": cap_dir = const.DOWN

        pivot_x = capman.rect.centerx // const.TILE_SIZE_X + (2 * cap_dir[0])
        pivot_y = capman.rect.centery // const.TILE_SIZE_Y + (2 * cap_dir[1])
        red_x = red_ghost.rect.centerx // const.TILE_SIZE_X
        red_y = red_ghost.rect.centery // const.TILE_SIZE_Y

        target_x = red_x + (pivot_x - red_x) * 2
        target_y = red_y + (pivot_y - red_y) * 2
        if 2>target_x:target_x=2
        if len(grid[0])-2<target_x: target_x = len(grid[0]) - 3
        if 2>target_y: target_y = 2
        if len(grid)-2<target_y: target_y = len(grid)-3
        return target_x, target_y

    def frighten(self):
        #funkcja do wywolania w przypadku zjedzenia
        #przez capmana duzego punkta
        self.mode="FRIGHTENED"
        self.speed=const.FRIGHTENED_SPEED

    def update(self, capman, red_ghost, time):
        #do wywolywania co obrot petli
        if capman is None or red_ghost is None: return
        
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

        is_inside_house = 5 < curr_tile_y < 12 and 19 < curr_tile_x < 24
        
        if is_inside_house:
            allowed = "anop"
            target_x_pixel = self.home_tile_x * const.TILE_SIZE_X + const.TILE_SIZE_X // 2
            
            if abs(self.rect.centerx - target_x_pixel) > self.speed:
                if self.rect.centerx < target_x_pixel:
                    self.direction = const.RIGHT
                    self.next_direction = const.RIGHT
                else:
                    self.direction = const.LEFT
                    self.next_direction = const.LEFT
            else:
                self.rect.centerx = target_x_pixel 
                self.direction = const.UP
                self.next_direction = const.UP
        
        else:
            allowed = "ano"
            
            if (curr_tile_x, curr_tile_y) != self.last_tile:
                
                if self.mode == "FRIGHTENED":
                    possible_dirs = []
                    for d in [const.UP, const.DOWN, const.LEFT, const.RIGHT]:
                        # Nie zawracaj
                        if d == (-self.direction[0], -self.direction[1]): continue
                        
                        nx, ny = curr_tile_x + d[0], curr_tile_y + d[1]
                        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] in allowed:
                            possible_dirs.append(d)
                    
                    if possible_dirs:
                        self.next_direction = random.choice(possible_dirs)
                    else:
                        self.next_direction = (-self.direction[0], -self.direction[1])

                else:
                    target_x, target_y = self.choose_target_tile(capman, red_ghost)
                    res = bfs(curr_tile_x, curr_tile_y, target_x, target_y, allowed, self.direction)
                    
                    if res and isinstance(res, tuple):
                        nx, ny = res
                        if nx > curr_tile_x: self.next_direction = const.RIGHT
                        elif nx < curr_tile_x: self.next_direction = const.LEFT
                        elif ny > curr_tile_y: self.next_direction = const.DOWN
                        elif ny < curr_tile_y: self.next_direction = const.UP
                    else:
                        if grid[curr_tile_y][curr_tile_x+1] in allowed: self.next_direction = const.RIGHT
                        elif grid[curr_tile_y][curr_tile_x-1] in allowed: self.next_direction = const.LEFT
                
                self.last_tile = (curr_tile_x, curr_tile_y)

            if self.direction != self.next_direction:
                if abs(self.rect.centerx - center_x) <= self.speed and abs(self.rect.centery - center_y) <= self.speed:
                    self.rect.center = (center_x, center_y)
                    self.direction = self.next_direction

        check_dist = 14
        check_x = int((self.rect.centerx + self.direction[0] * check_dist) // const.TILE_SIZE_X)
        check_y = int((self.rect.centery + self.direction[1] * check_dist) // const.TILE_SIZE_Y)

        can_move = False
        if 0 <= check_y < len(grid) and 0 <= check_x < len(grid[0]):
            if grid[check_y][check_x] in allowed:
                can_move = True
        
        if can_move:
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed
        else:
            if not is_inside_house:
                self.last_tile = (-1, -1)
                for d in [const.UP, const.LEFT, const.RIGHT, const.DOWN]:
                    if d == (-self.direction[0], -self.direction[1]): continue 
                    tx = int((self.rect.centerx + d[0] * 20) // const.TILE_SIZE_X)
                    ty = int((self.rect.centery + d[1] * 20) // const.TILE_SIZE_Y)
                    if 0 <= ty < len(grid) and 0 <= tx < len(grid[0]) and grid[ty][tx] in allowed:
                        self.direction = d
                        self.next_direction = d
                        break
            else:
                if self.direction == const.DOWN: 
                    self.direction = const.UP
                    self.next_direction = const.UP
    def collision(self, capman):
        #do wywolania w przypadku kolizji inkiego z capmanem
        if self.mode == "EATEN": return False
        if self.mode == "FRIGHTENED":
            self.mode="EATEN"
            self.speed=const.EATEN_SPEED
        return self.rect.colliderect(capman.rect)