import pygame as p
from sys import exit
from CONST import *
#Stworzenie klasy CapMan
class CapMan(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #Ilość serduszek
        self.hearts = 2
        #Prędkość z jaką Cap-Man będzie się poruszał (pixels per frame)
        self.speed = 1
        #Pomocniczy obrazek, do zmiany
        self.angle = 0
        self.image = p.image.load('../zdj/cap_man_1.png').convert_alpha()
        self.image = p.transform.scale(self.image,(45,45))
        #Podstawowa pozycja Cap - Mana
        self.rect = self.image.get_rect(center = (200,500))
    def player_movement(self, pressed_key):
        #Porusza się w odpowiednim kierunku pod warunkiem że środek jest na ekranie
        #Oraz nie zostanie wciśnięty inny klawisz
        if (pressed_key == p.K_UP or pressed_key == p.K_w):
            self.rect.y -= self.speed
        elif (pressed_key == p.K_DOWN or pressed_key == p.K_s):
            self.rect.y += self.speed
        elif (pressed_key == p.K_RIGHT or pressed_key == p.K_d):
            self.rect.x += self.speed
        elif (pressed_key == p.K_LEFT or pressed_key == p.K_a):
            self.rect.x -= self.speed
    def player_rotation(self,pressed_key):
        #Oraz nie zostanie wciśnięty inny klawisz
        # 0 stopni - porusza się w prawo
        # 90 stopni - porusza się w dół
        # 270 stopni - porusza się w górę
        # 180 stopni - porusza się w lewo
        # rotated = p.transform.rotate(self.image, self.angle)
        if (pressed_key == p.K_UP or pressed_key == p.K_w):
            if self.angle == 90:
                self.image = p.transform.flip(self.image,False, True)
            elif self.angle == 0:
                self.image = p.transform.rotate(self.image, 90)
            elif self.angle == 180:
                self.image = p.transform.rotate(self.image, -90)
                self.image = p.transform.flip(self.image,True, False)
            self.angle = 270
        elif (pressed_key == p.K_DOWN or pressed_key == p.K_s):
            if self.angle == 0:
                self.image = p.transform.rotate(self.image, -90)
                self.image = p.transform.flip(self.image,True, False)
            elif self.angle == 270:
                self.image = p.transform.flip(self.image,False, True)
            elif self.angle == 180:
                self.image = p.transform.rotate(self.image, 90)
            self.angle = 90
        elif (pressed_key == p.K_RIGHT or pressed_key == p.K_d):
            if self.angle == 180:
                self.image = p.transform.flip(self.image,True, False)
            elif self.angle == 270:
                self.image = p.transform.rotate(self.image, -90)
            elif self.angle == 90:
                self.image = p.transform.flip(self.image,False, True)
                self.image = p.transform.rotate(self.image, -90)
            self.angle = 0
        elif (pressed_key == p.K_LEFT or pressed_key == p.K_a):
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
        #Zwraca obecnie wciśnięty klawisz, jeżeli jest jednym z tych które bierzemy pod uwagę
        keys = p.key.get_pressed()
        if keys[p.K_UP] or keys[p.K_w]:
            return p.K_UP
        elif keys[p.K_DOWN] or keys[p.K_s]:
            return p.K_DOWN
        elif keys[p.K_RIGHT] or keys[p.K_d]:
            return p.K_RIGHT
        elif keys[p.K_LEFT] or keys[p.K_a]:
            return p.K_LEFT
        return None
    #Zmienia kierunek poruszania się postaci
    def update(self,pressed_key):
        self.player_movement(pressed_key)
        #Teleport Cap-Mana
        #40px od prawej krawędzi ekranu, i 10 od lewej
        if self.rect.centerx > WIDTH - 40:
            self.rect.centerx = 10
        elif self.rect.centerx < 10:
            self.rect.centerx = WIDTH - 40
    #Funkcje do zwiększenia i zmniejszenia prędkości 
    def increase_speed(self):
        self.speed += 1
    def reduce_speed(self):
        self.speed -= 1

