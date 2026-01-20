"""
clyde - pomaranczowy duszek

jesli > 8 pol - chase jak blinky
jesli < 8 pol - kieruje sie do rogu mapy (lewy dolny)

"""

import pygame
import random
import CONST as const
from board import board as grid
from collections import deque

#bfs
def bfs(start_x, start_y, target_x, target_y, allowed, flag):
    queue = deque([(start_x, start_y, [(start_x, start_y)])])
    visited = set([(start_x, start_y)])
    while queue:
        curr_x, curr_y, path = queue.popleft()
        if curr_x == target_x and curr_y == target_y: 
            if flag: return len(path)
            return path[1] if len(path) > 1 else path[0]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = curr_x + dx, curr_y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and (nx, ny) not in visited and grid[ny][nx] in allowed:
                visited.add((nx, ny))
                queue.append((nx, ny, path + [(nx, ny)]))
    return None

class Clyde(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.home_x, self.home_y = 22.5*const.TILE_SIZE_X, 9.5*const.TILE_SIZE_Y
        self.direction = const.LEFT
        self.mode = "SCATTER"
        self.speed = const.CLYDE_SPEED
        self.cooldown = 0

        #obrazek
        self.angle = 0
        self.image = pygame.image.load("cap_man_1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 45))

        self.rect = self.image.get_rect(center = (self.home_x, self.home_y))

    def get_target(self, pacman):
        if self.mode == "SCATTER": return 2, 26
        if self.mode == "FRIGHTEND": return -1, -1
        if self.mode == "EATEN": return self.home_x, self.home_y
        clyde_tile_x = self.rect.centerx // const.TILE_SIZE_X
        clyde_tile_y = self.rect.centery // const.TILE_SIZE_Y
        pacman_tile_x = pacman.rect.centerx // const.TILE_SIZE_X
        pacman_tile_y = pacman.rect.centery // const.TILE_SIZE_Y
        allowed = "ano" if self.mode == "CHASE" else "anop" 
        length = bfs(clyde_tile_x, clyde_tile_y, pacman_tile_x, pacman_tile_y, allowed, 1)
        if length > 8: return pacman_tile_x, pacman_tile_y
        return 2, 26

    #zamian trybu wzgledem czasu
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

    def possible_moves(self):
        moves = [False, False, False, False] #right left up down
        
        num1 = const.TILE_SIZE_Y
        num2 = const.TILE_SIZE_X
        num3 = num2 // 2

        max_y = len(grid)
        max_x = len(grid[0])

        def possible(y, x):
            if 0 <= y <= max_y:
                x = x%max_x
                if self.mode == "CHASE": return grid[y][x] in "ano"
                else: return grid[y][x] in "anop"
            return False

        #indeksy w ktorym jest srodek duszka
        tile_x = self.rect.centerx // num2
        tile_y = self.rect.centery // num1

        if tile_x < max_x - 1:
            #ruch w prawo
            moves[0] = possible(tile_y, (self.rect.centerx + num3) // num2) and self.direction != const.LEFT
            #ruch w lewo
            moves[1] = possible(tile_y, (self.rect.centerx - num3) // num2) and self.direction != const.RIGHT
            #ruch w gore
            moves[2] = possible((self.rect.centery - num3) // num1, self.rect.centerx // num2) and self.direction != const.DOWN
            #ruch w dol
            moves[3] = possible((self.rect.centery + num3) // num1, self.rect.centerx // num2) and self.direction != const.UP
        else:
            moves[0] = moves[1] = True
        return moves

    #wykonanie ruchu
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

    def update(self, pacman, time):
        #aktualizacja trybu
        self.mode_update(time)

        #mozliwe ruchy #right left up down
        moves = self.possible_moves()

        #gdzie idziemy
        target_x, target_y = self.get_target(pacman)

        if target_x == -1 and target_y == -1:
            self.move(random.choice(moves))
            return
        
        tile_x = self.rect.centerx // const.TILE_SIZE_X
        tile_y = self.rect.centery // const.TILE_SIZE_Y
        direction = None


        allowed = "ano" if self.mode == "CHASE" else "anop" 
        goto = bfs(tile_x, tile_y, target_x, target_y, allowed, 0)
        goto_x, goto_y = goto

        for i in range(4):
            if not moves[i]: continue
            new_x = tile_x if const.DIRECTIONS[i] == 0 else (self.rect.centerx + (const.TILE_SIZE_X)*const.DIRECTIONS[i][0]) // const.TILE_SIZE_X
            new_y = tile_y if const.DIRECTIONS[i] == 0 else (self.rect.centery + (const.TILE_SIZE_Y)*const.DIRECTIONS[i][1]) // const.TILE_SIZE_Y
            if new_x == goto_x and new_y == goto_y: 
                direction = const.DIRECTIONS[i]
        self.move(direction)

        #tunel
        if self.rect.centerx > const.WIDTH - 10: self.rect.centerx = 10
        elif self.rect.centerx < 10: self.rect.centerx = const.WIDTH - 10
        return None

    #sprawdzenie kolizji
    def collision(self, pacman):
        pinky_tile_x = self.rect.centerx // const.TILE_SIZE_X
        pinky_tile_y = self.rect.centery // const.TILE_SIZE_Y

        pacman_tile_x = pacman.rect.centerx // const.TILE_SIZE_X
        pacman_tile_y = pacman.rect.centery // const.TILE_SIZE_Y

        return ((pinky_tile_x == pacman_tile_x) and (pinky_tile_y == pacman_tile_y))
    
    def scared(self):
        self.mode = "FRIGHTEND"
        self.speed = const.FRIGHTENED_SPEED
        #zmiana grafiki
    
    def unscared(self, time):
        self.mode = "CHASE"
        self.mode_update(time)
        self.speed = const.PINKY_SPEED