import pygame as p
import sys
from CONST import *
from button import Button

p.init()

screen = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Main menu")
main_background = p.image.load("images/background.png")
main_background = p.transform.scale(main_background, (WIDTH, HEIGHT))
blinky = p.image.load("images/blinky/blinky_right_2.png")
blinky = p.transform.scale(blinky, (90, 90))
clyde = p.image.load("images/clyde/clyde_right_2.png")
clyde = p.transform.scale(clyde, (90, 90))
inky = p.image.load("images/inky/inky_right_2.png")
inky = p.transform.scale(inky, (90, 90))
pinky = p.image.load("images/pinky/pinky_right_2.png")
pinky = p.transform.scale(pinky, (90, 90))
cap_man = p.image.load("images/cap_man_1_1.png")
cap_man = p.transform.scale(cap_man, (90, 90))

play_button = Button(WIDTH/2-(250/2), 410, 250, 70, "PLAY", "images/button.png", "images/button_hover.png")
exit_button = Button(WIDTH/2-(250/2), 510, 250, 70, "EXIT", "images/button.png", "images/button_hover.png")

def main_menu():
    running = True
    while running:
        screen.fill((0,0,0))
        screen.blit(main_background, (0,0))
        screen.blit(blinky, (325,716))
        screen.blit(clyde, (425,716))
        screen.blit(inky, (525,716))
        screen.blit(pinky, (625,716))
        screen.blit(cap_man, (850,716))

        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
                p.quit()
                sys.exit()
            if event.type == p.USEREVENT and event.button == exit_button:
                running = False
                p.quit()
                sys.exit()
            for btn in [play_button, exit_button]:
                btn.handle_event(event)

        for btn in [play_button, exit_button]:
            btn.check_hover(p.mouse.get_pos())
            btn.draw(screen)
        p.display.flip()

main_menu()