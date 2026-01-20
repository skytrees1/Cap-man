import pygame as p
from sys import exit
from CONST import *
from hero import CapMan

p.init()

screen = p.display.set_mode((920,680))
clock = p.time.Clock()
running = True

#Stworzenie naszej postaci, przed główną pętlą gry
player = p.sprite.GroupSingle()
player.add(CapMan())
while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
            exit()
        #Sprawdza czy wcisneliśmy jakiś przycisk
        if event.type == p.KEYDOWN:
            #Przypisuje klawisz jaki wcisneliśmy do zmiennej last_key
            last_direction = player.sprite.checking_Pressed_Keys()
            #Last_key = None wtw gdy nie jest to klawisz odpowiadający za zmiane kierunku (strzałki albo WASD)
            if last_direction != None and last_direction != player.sprite.direction:
                player.sprite.direction = last_direction
                player.sprite.player_rotation(player.sprite.direction)
    screen.fill("Purple")
    #Narysowanie Cap-Mana na ekranie
    player.draw(screen)
    #Aktualizuje co robimy z naszą postacią
    player.update(player.sprite.direction)
    p.display.flip()
    #Ustawia maks FPS, prędkość obiektów jest zależna od ilości FPS
    clock.tick(60)
p.quit()