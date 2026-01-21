#Pinky - różowy duszek
#Strategia:
#Patrzy 4 pola przed pacmana

import pygame
import random
import CONST as const
from board import board as grid
from collections import deque

#bfs
#zwraca (x,y) pola na które należy przejść w kierunku celu
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
        #tunel
        if curr_x == 0 and (40, curr_y) not in visited: queue.append((40, curr_y, path + [(40, curr_y)]))
        if curr_x == 40 and (0, curr_y) not in visited: queue.append((0, curr_y, path + [(0, curr_y)]))
    return None


#stworzenie klasy duszka

class Pinky(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.home_x, self.home_y = 23.5*const.TILE_SIZE_X, 9*const.TILE_SIZE_Y #wspolrzedne poczatkowe
        self.direction = const.LEFT #kierunek poczatkowy
        self.mode = "SCATTER" #tryb poczatkowy
        self.speed = const.PINKY_SPEED
        self.cooldown = 0 #cooldown po zjedeniu

        #obrazek
        self.angle = 0
        self.image = pygame.image.load("assets/images/pinky/pinky_down_1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 45))

        #wspolrzedne startowe
        self.rect = self.image.get_rect(center = (self.home_x, self.home_y))
        #self.home_x = self.rect.centerx
        #self.home_y = self.rect.centery

    #wyznaczenie pola w kierunku ktorego idzie duszek w zaleznosci od trybu
    def get_target(self, pacman):
        #jezeli SCATTER to idzie do lewego gornego
        if self.mode == "SCATTER": return 2, 2
        #jezeli FRIGHTENED to losowy ruch
        if self.mode == "FRIGHTENED": return -1, -1
        #jezeli EATEN to wraca do domu
        if self.mode == "EATEN": return self.home_x // const.TILE_SIZE_X, self.home_y // const.TILE_SIZE_Y
        #jezeli CHASE to mierzy 4 pola przed pacmana
        dir = None
        if pacman.capman_direction == None: dir = const.LEFT
        elif pacman.capman_direction == "move_right": dir = const.RIGHT
        elif pacman.capman_direction == "move_left": dir = const.LEFT
        elif pacman.capman_direction == "move_up": dir = const.UP
        elif pacman.capman_direction == "move_down": dir = const.DOWN
        target_x = pacman.rect.centerx + 4*dir[0]
        target_y = pacman.rect.centery + 4*dir[1]
        while target_x > const.WIDTH or target_y > const.HEIGHT or grid[target_y // const.TILE_SIZE_Y][target_x // const.TILE_SIZE_X] not in "anop":
            target_x -= dir[0]
            target_y -= dir[1]
        return target_x // const.TILE_SIZE_X, target_y // const.TILE_SIZE_Y
    
    #zamian trybu wzgledem czasu
    def mode_update(self, time):
        if self.mode == "FRIGHTENED": return
        if self.mode == "EATEN":
            if self.rect.centerx == self.home_x and self.rect.centery == self.home_y and self.cooldown != 0: self.cooldown -= 1
            if self.rect.centerx == self.home_x and self.rect.centery == self.home_y and self.cooldown == 0:
                self.speed = const.PINKY_SPEED
                self.mode = "SCATTER"
            return
        elif 0 < time <= 7: self.mode = "SCATTER"
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
                if x >= max_x: return 1
                #x = x%max_x
                if self.mode == "CHASE": return grid[y][x] in "anop"
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

    #wyznaczenie ruchu
    def update(self, pacman, time):
        #aktualizacja trybu
        self.mode_update(time)

        #mozliwe ruchy #right left up down
        moves = self.possible_moves()

        #gdzie idziemy
        target_x, target_y = self.get_target(pacman)
        #print(target_x, target_y)

        if target_x == -1 and target_y == -1: #losowy ruch
            directions = []
            if moves[0] and self.direction != const.LEFT: directions.append(const.RIGHT)
            if moves[1] and self.direction != const.RIGHT: directions.append(const.LEFT)
            if moves[2] and self.direction != const.DOWN: directions.append(const.UP)
            if moves[3] and self.direction != const.UP: directions.append(const.DOWN)
            if self.direction in directions: self.move(self.direction)
            else: self.move(random.choice(directions))
            #tunel
            if self.rect.centerx > const.WIDTH - 10: self.rect.centerx = 10
            elif self.rect.centerx < 10: self.rect.centerx = const.WIDTH - 10
            return
        
        tile_x = self.rect.centerx // const.TILE_SIZE_X
        tile_y = self.rect.centery // const.TILE_SIZE_Y
        direction = None

        allowed = "anop" if self.mode == "CHASE" else "anop" 
        goto = bfs(tile_x, tile_y, target_x, target_y, allowed)
        goto_x, goto_y = goto

        for i in range(4):
            #if not moves[i]: continue
            new_x = tile_x if const.DIRECTIONS[i] == 0 else (self.rect.centerx + (const.TILE_SIZE_X)*const.DIRECTIONS[i][0]) // const.TILE_SIZE_X
            new_y = tile_y if const.DIRECTIONS[i] == 0 else (self.rect.centery + (const.TILE_SIZE_Y)*const.DIRECTIONS[i][1]) // const.TILE_SIZE_Y
            if new_x == goto_x and new_y == goto_y: 
                direction = const.DIRECTIONS[i]
        if tile_x == 0 and goto_x == 40: direction = const.LEFT
        if tile_x == 40 and goto_x == 0: direction = const.RIGHT

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
        self.mode = "FRIGHTENED"
        self.speed = const.FRIGHTENED_SPEED
        #zmiana grafiki
    
    def unscared(self, time):
        if self.mode == "EATEN": return
        self.mode = "CHASE"
        self.mode_update(time)
        self.speed = const.PINKY_SPEED