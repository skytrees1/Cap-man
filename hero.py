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
        self.speed = 2
        #Pomocniczy obrazek, do zmiany
        self.image = p.image.load('../zdj/cap_man_1.png').convert_alpha()
        #Podstawowa pozycja Cap - Mana
        self.rect = self.image.get_rect(center = (200,500))
    def player_movement(self, pressed_key):
        #Porusza się w odpowiednim kierunku pod warunkiem że środek jest na ekranie
        #Oraz nie zostanie wciśnięty inny klawisz
        if (pressed_key == p.K_UP or pressed_key == p.K_w) and self.rect.centery > 0:
            self.rect.y -= self.speed
        elif (pressed_key == p.K_DOWN or pressed_key == p.K_s) and self.rect.centery < 680:
            self.rect.y += self.speed
        elif (pressed_key == p.K_RIGHT or pressed_key == p.K_d) and self.rect.centerx > 0:
            self.rect.x += self.speed
        elif (pressed_key == p.K_LEFT or pressed_key == p.K_a) and self.rect.centerx < 920:
            self.rect.x -= self.speed
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
    def update(self,pressed_key):
        self.player_movement(pressed_key)
    #Funkcje do zwiększenia i zmniejszenia prędkości 
    def increase_speed(self):
        self.speed += 2
    def reduce_speed(self):
        self.speed -= 2

        
