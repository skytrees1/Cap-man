import pygame as p
import sys
from CONST import *
from button import Button

p.init()

screen = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Main menu")

play_button = Button(WIDTH/2-(250/2), 450, 250, 70, "PLAY", "images\\button.png", "images\\button_hover.png")
exit_button = Button(WIDTH/2-(250/2), 600, 250, 70, "EXIT", "images\\button.png", "images\\button_hover.png")

def main_menu():
    running = True
    while running:
        screen.fill((0,0,0))

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