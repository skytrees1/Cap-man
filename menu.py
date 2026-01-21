import pygame as p
import sys
from CONST import *
from button import Button

p.init()

screen = p.display.set_mode((WIDTH, HEIGHT), p.RESIZABLE)
game_screen = p.Surface((WIDTH, HEIGHT))

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
        game_screen.fill((0,0,0))
        game_screen.blit(main_background, (0,0))
        game_screen.blit(blinky, (325,716))
        game_screen.blit(clyde, (425,716))
        game_screen.blit(inky, (525,716))
        game_screen.blit(pinky, (625,716))
        game_screen.blit(cap_man, (850,716))

        curr_w, curr_h = screen.get_size()
        # Oblicz współczynnik skali
        scale_x = WIDTH / curr_w
        scale_y = HEIGHT / curr_h

        # Pobierz pozycję myszy i ją przelicz
        mouse_pos = p.mouse.get_pos()
        adjusted_mouse_pos = (mouse_pos[0] * scale_x, mouse_pos[1] * scale_y)

        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
                p.quit()
                sys.exit()

            if event.type == p.USEREVENT:
                if event.button == play_button:
                    return "PLAY"
                if event.button == exit_button:
                    return "EXIT"
                
            for btn in [play_button, exit_button]:
                btn.handle_event(event, adjusted_mouse_pos)

        for btn in [play_button, exit_button]:
            btn.check_hover(adjusted_mouse_pos)
            btn.draw(game_screen)
         # skalowanie obrazu 
    
        scaled_surface = p.transform.smoothscale(game_screen, (curr_w, curr_h))
        screen.blit(scaled_surface, (0, 0))

        p.display.flip()

