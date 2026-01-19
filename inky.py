import pygame as p
import math
import CONST as const
from board import board as grid
from hero import Capman as capman
from red import red
import random

def bfs(start_x, start_y, target_x, target_y, allowed):
    queue = deque([(start_x, start_y, [(start_x, start_y)])])
    visited = set([(start_x, start_y)])
    while queue:
        curr_x, curr_y, path = queue.popleft()
        if curr_x == target_x and curr_y == target_y: 
            return path[1] if len(path) > 1 else path[0]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = curr_x + dx, curr_y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and (nx, ny) not in visited and grid[ny][nx] in allowed:
                visited.add((nx, ny))
                queue.append((nx, ny, path + [(nx, ny)]))
    return None

class inky(p.sprite.Sprite):
    def __init__(self):
        super().__init()
        self.direction=const.RIGHT
        self.home_x = 24.5*const.TILE_SIZE_X
        self.home_y = 8.5*const.TILE_SIZE_Y
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

    def pos_moves(self):
        moves = [False, False, False, False]

        max_x = len(grid)
        max_y = len(grid[0])
        
        num1 = const.TILE_SIZE_Y
        num2=const.TILE_SIZE_X//2

        def pos(y, x):
            if 0 <= y <=max_y:
                x=x%max_x
                if self.mode=="CHASE":
                    return grid[y][x] in "ano"
                else:
                    return grid[y][x] in "anop"
            return False

        tile_x = self.rect.centerx // num2
        tile_y = self.rect.centery // num1
        num3=num2//2

        if tile_x < max_x - 1:
            #ruch w prawo
            moves[0] = pos(tile_y, (self.rect.centerx + num3) // num2) and self.direction != const.LEFT
            #ruch w lewo
            moves[1] = pos(tile_y, (self.rect.centerx - num3) // num2) and self.direction != const.RIGHT
            #ruch w gore
            moves[2] = pos((self.rect.centery - num3) // num1, self.rect.centerx // num2) and self.direction != const.DOWN
            #ruch w dol
            moves[3] = pos((self.rect.centery + num3) // num1, self.rect.centerx // num2) and self.direction != const.UP
        else:
            moves[0] = moves[1] = True
        return moves
    def choose_target_tile(self, capman, red):
        if self.mode=="FRIGHTENED":
            return -1, -1
        if self.mode=="EATEN":
            return self.home_x//const.TILE_SIZE_X, self.home_y//const.TILE_SIZE_Y
        if self.mode=="SCATTER":
            return len(grid[0])-2, len(grid)-2
        if capman.capman_direction == None: dir = const.LEFT
        elif capman.capman_direction == "move_right": dir = const.RIGHT
        elif capman.capman_direction == "move_left": dir = const.LEFT
        elif capman.capman_direction == "move_up": dir = const.UP
        elif capman.capman_direction == "move_down": dir = const.DOWN
        vector_mid_x = capman.rect.centerx//const.TILE_SIZE_X + 2*dir[1]
        vector_mid_y = capman.rect.centery//const.TILE_SIZE_Y + 2*dir[0]

        vector_start_x = red.rect.centerx//const.TILE_SIZE_X
        vector_start_y = red.rect.centery//const.TILE_SIZE_Y

        vector_x = vector_mid_x-vector_start_x
        vector_y = vector_mid_y-vector_start_y
        vector_x*=2
        vector_y*=2
        target_x = vector_start_x+vector_x
        target_y = vector_start_y+vector_y
        if target_x>=len(grid[0]): target_x = len(grid[0])-1
        if target_x<0: target_x=0
        if target_y>=len(grid): target_y=len(grid)-1
        if target_y<0: target_y=0
        return target_x, target_y
    def choose_next_tile(self, capman):
        if self.rect.x % const.TILE_SIZE_X != 0: return
        if self.rect.y % const.TILE_SIZE_Y != 0: return
 
        target_x, target_y = self.choose_target_tile(capman)
        moves = self.pos_moves
        if target_x==-1 and target_y==-1:
            return random.choice(moves)
        if self.mode=="CHASE":
            allowed = "ano"
        else:
            allowed = "anop"
        next = bfs(self.rect.centerx//const.TILE_SIZE_X, self.rect.centery//const.TILE_SIZE_Y, target_x, target_y, allowed)
        next_x, next_y = next

        for i in (0, 4):
            if moves[i]==False:
                continue
            temp_x = next_x if const.DIRECTIONS[i]==0 else (self.rect.centerx + (const.TILE_SIZE_X)*const.DIRECTIONS[i][0]) // const.TILE_SIZE_X
            temp_y = next_y if const.DIRECTIONS[i] == 0 else (self.rect.centery + (const.TILE_SIZE_Y)*const.DIRECTIONS[i][1]) // const.TILE_SIZE_Y
            if temp_x==next_x and temp_y==next_y:
                return const.DIRECTIONS[i]
        return None
    
    def move(self, direction):
        center_x = (self.rect.centerx // const.TILE_SIZE_X) * const.TILE_SIZE_X + (const.TILE_SIZE_X // 2)
        center_y = (self.rect.centery // const.TILE_SIZE_Y) * const.TILE_SIZE_Y + (const.TILE_SIZE_Y // 2)

        if direction == const.RIGHT:
            self.rect.x += self.speed
            self.rect.centery = center_y
        elif direction == const.LEFT:
            self.rect.x -= self.speed
            self.rect.centery = center_y
        elif direction == const.UP:
            self.rect.y -= self.speed
            self.rect.centerx = center_x
        elif direction == const.DOWN:
            self.rect.y += self.speed
            self.rect.centerx = center_x
        self.direction = direction

    def collision(self, capman):
        if self.mode=="EATEN":
            return False
        red_tile_x = self.rect.centerx // const.TILE_SIZE_X
        red_tile_y = self.rect.centery // const.TILE_SIZE_Y

        capman_tile_x = capman.rect.centerx // const.TILE_SIZE_X
        capman_tile_y = capman.rect.centery // const.TILE_SIZE_Y

        return ((red_tile_x == capman_tile_x) and (red_tile_y == capman_tile_y))
    def scared(self):
        self.mode = "FRIGHTEND"
        self.speed = const.FRIGHTENED_SPEED
    def scared_stop(self, time):
        self.mode=="CHASE"
        self.mode_update
        self.speed=const.PINKY_SPEED
    def update(self, capman, red, time):
        self.mode_update(time)

        if self.rect.x % const.TILE_SIZE_X != 0 and self.rect.y % const.TILE_SIZE_Y != 0:
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed
            return
        
        target_x, target_y = self.choose_target_tile(capman, red)

        if self.mode=="CHASE" or self.mode=="SCATTER":
            self.speed=const.PINKY_SPEED
        if self.mode=="FRIGHTENED":
            self.speed = const.FRIGHTENED_SPEED
        if self.mode=="EATEN":
            self.speed=const.EATEN_SPEED

        direction = self.choose_next_tile
        
        self.move(direction)

        if self.mode == "EATEN" and abs(self.rect.x - self.home_x) < 2 and abs(self.rect.y - self.home_y) < 2: 
            self.mode == "SCATTER"
            self.cooldown = 5 





