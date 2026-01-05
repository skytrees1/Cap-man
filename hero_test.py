import pygame as p
from sys import exit
from CONST import *
from hero import CapMan

p.init()

screen = p.display.set_mode((920,680))
clock = p.time.Clock()
running = True
#Potrzebna zmienna nr.1
# PRESSED_KEY = None
#Stworzenie naszej postaci, przed główną pętlą gry
player = p.sprite.GroupSingle()
player.add(CapMan())
while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
            exit()
        #Potrzebne do poprawnego funkcjonowania
        if event.type == p.KEYDOWN:
            last_key = player.sprite.checking_Pressed_Keys()
            if last_key != None:
                PRESSED_KEY = last_key
    screen.fill("Purple")
    #Narysowanie Cap-Mana na ekranie
    player.draw(screen)
    #Aktualizuje co robimy z naszą postacią
    player.update(PRESSED_KEY)
    #
    p.display.flip()
    #Testowe odwołanie się do zmiennej hearts oraz zmiana jej wartości
    #Po podanym warunku Postać się zatrzymuje (pressed_key = None) i potem można dalej ustawić kierunek
    # player.sprite.hearts -= 1
    # if player.sprite.hearts  == -150:
    #Poprawnie działa increase_speed()
        # player.sprite.increase_speed()
    #     pressed_key = None
    # print(player.sprite.hearts)
    clock.tick(60)
p.quit()