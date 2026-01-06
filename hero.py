import pygame as p
from sys import exit
from CONST import *
from map_generator import level
#Stworzenie klasy CapMan
class CapMan(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #Kierunek postaci
        self.capman_direction = None
        #Ilość serduszek
        self.hearts = 2
        #Prędkość z jaką Cap-Man będzie się poruszał (pixels per frame)
        self.speed = 1
        #Pomocniczy obrazek, do zmiany
        self.angle = 0
        self.image = p.image.load('cap_man_1.png').convert_alpha()
        self.image = p.transform.scale(self.image,(45,45))
        #Podstawowa pozycja Cap - Mana na obecnej mapie
        self.rect = self.image.get_rect(center = (STARTING_POSITION_X,STARTING_POSITION_Y))
    def player_movement(self, direction,turns):
        #Porusza się w odpowiednim kierunku pod warunkiem że środek jest na ekranie
        #Oraz nie zostanie wciśnięty inny klawisz
        if direction == "move_up" and turns[2]:
            self.rect.y -= self.speed
        elif direction == "move_down" and turns[3]:
            self.rect.y += self.speed
        elif direction == "move_right" and turns[0]:
            self.rect.x += self.speed
        elif direction == "move_left" and turns[1]:
            self.rect.x -= self.speed
    def player_rotation(self,direction):
        #Oraz nie zostanie wciśnięty inny klawisz
        # 0 stopni - porusza się w prawo
        # 90 stopni - porusza się w dół
        # 270 stopni - porusza się w górę
        # 180 stopni - porusza się w lewo
        # rotated = p.transform.rotate(self.image, self.angle)
        turns = self.check_position(direction)
        if direction == "move_up" and turns[2]:
            if self.angle == 90:
                self.image = p.transform.flip(self.image,False, True)
            elif self.angle == 0:
                self.image = p.transform.rotate(self.image, 90)
            elif self.angle == 180:
                self.image = p.transform.rotate(self.image, -90)
                self.image = p.transform.flip(self.image,True, False)
            self.angle = 270
        elif direction == "move_down" and turns[3]:
            if self.angle == 0:
                self.image = p.transform.rotate(self.image, -90)
                self.image = p.transform.flip(self.image,True, False)
            elif self.angle == 270:
                self.image = p.transform.flip(self.image,False, True)
            elif self.angle == 180:
                self.image = p.transform.rotate(self.image, 90)
            self.angle = 90
        elif direction == "move_right" and turns[0]:
            if self.angle == 180:
                self.image = p.transform.flip(self.image,True, False)
            elif self.angle == 270:
                self.image = p.transform.rotate(self.image, -90)
            elif self.angle == 90:
                self.image = p.transform.flip(self.image,False, True)
                self.image = p.transform.rotate(self.image, -90)
            self.angle = 0
        elif direction == "move_left" and turns[1]:
            if self.angle == 0:
                self.image = p.transform.flip(self.image,True, False)
            elif self.angle == 90:
                self.image = p.transform.rotate(self.image, -90)
            elif self.angle == 270:
                self.image = p.transform.rotate(self.image, -90)
                self.image = p.transform.flip(self.image,True, False)
            self.angle = 180
    @staticmethod
    def checking_Pressed_Keys():
        #Zwraca obecnie kierunek, jeżeli jest jednym z tych które bierzemy pod uwagę
        keys = p.key.get_pressed()
        if keys[p.K_UP] or keys[p.K_w]:
            return "move_up"
        elif keys[p.K_DOWN] or keys[p.K_s]:
            return "move_down"
        elif keys[p.K_RIGHT] or keys[p.K_d]:
            return "move_right"
        elif keys[p.K_LEFT] or keys[p.K_a]:
            return "move_left"
        return None
    #Zmienia kierunek poruszania się postaci
    def update(self, direction):
        turns = self.check_position(direction)
        self.player_movement(direction, turns)

        # TELEPORT TUNELU 
        if self.rect.centerx > WIDTH - 40:
            self.rect.centerx = 10
        elif self.rect.centerx < 10:
            self.rect.centerx = WIDTH - 40
        
    #Funkcje do zwiększenia i zmniejszenia prędkości 
    def increase_speed(self):
        self.speed += 1
    def reduce_speed(self):
        self.speed -= 1
    def check_position(self, direction):
        # Czy postać może poruszyć się w Prawo,Lewo, Górę, Dół
        turns = [False, False, False, False]
        num_help = 15

        max_y = len(level)
        max_x = len(level[0])

        def safe_check(y, x):
            # y musi być w zakresie, x możemy zawinąć (tunel)
            if 0 <= y < max_y:
                x_wrapped = x % max_x
                return level[y][x_wrapped] in ('a', 'o', 'n')
            return False

        if self.rect.centerx // 30 < 29:
            if direction == "move_right":
                if safe_check(self.rect.centery // TILE_SIZE_Y,
                            (self.rect.centerx + num_help) // TILE_SIZE_X):
                    turns[0] = True

            if direction == "move_left":
                if safe_check(self.rect.centery // TILE_SIZE_Y,
                            (self.rect.centerx - num_help) // TILE_SIZE_X):
                    turns[1] = True

            if direction == "move_up":
                if safe_check((self.rect.centery - num_help) // TILE_SIZE_Y,
                            self.rect.centerx // TILE_SIZE_X):
                    turns[2] = True

            if direction == "move_down":
                if safe_check((self.rect.centery + num_help) // TILE_SIZE_Y,
                            self.rect.centerx // TILE_SIZE_X):
                    turns[3] = True

            if direction == "move_up" or direction == "move_down":
                if (TILE_SIZE_X // 2) - 3 <= self.rect.centerx % TILE_SIZE_X <= (TILE_SIZE_X // 2) + 3:
                    if safe_check((self.rect.centery + num_help)//TILE_SIZE_Y,
                                self.rect.centerx // TILE_SIZE_X):
                        turns[3] = True
                    if safe_check((self.rect.centery - num_help)//TILE_SIZE_Y,
                                self.rect.centerx // TILE_SIZE_X):
                        turns[2] = True

                if (TILE_SIZE_Y // 2) - 3 <= self.rect.centery % TILE_SIZE_Y <= (TILE_SIZE_Y // 2) + 3:
                    if safe_check(self.rect.centery//TILE_SIZE_Y,
                                (self.rect.centerx - TILE_SIZE_X) // TILE_SIZE_X):
                        turns[1] = True
                    if safe_check(self.rect.centery//TILE_SIZE_Y,
                                (self.rect.centerx + TILE_SIZE_X) // TILE_SIZE_X):
                        turns[0] = True

            if direction == "move_right" or direction == "move_left":
                if (TILE_SIZE_X // 2) - 3 <= self.rect.centerx % TILE_SIZE_X <= (TILE_SIZE_X // 2) + 3:
                    if safe_check((self.rect.centery + TILE_SIZE_Y)//TILE_SIZE_Y,
                                self.rect.centerx // TILE_SIZE_X):
                        turns[3] = True
                    if safe_check((self.rect.centery - TILE_SIZE_Y)//TILE_SIZE_Y,
                                self.rect.centerx // TILE_SIZE_X):
                        turns[2] = True

                if (TILE_SIZE_Y // 2) - 3 <= self.rect.centery % TILE_SIZE_Y <= (TILE_SIZE_Y // 2) + 3:
                    if safe_check(self.rect.centery//TILE_SIZE_Y,
                                (self.rect.centerx - num_help) // TILE_SIZE_X):
                        turns[1] = True
                    if safe_check(self.rect.centery//TILE_SIZE_Y,
                                (self.rect.centerx + num_help) // TILE_SIZE_X):
                        turns[0] = True
        else:
            turns[0] = True
            turns[1] = True

        return turns
