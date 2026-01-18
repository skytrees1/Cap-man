import pygame
import copy
from board import board as grid
import CONST as const
from map_generator import draw_map
from sys import exit
from pinky import Pinky
from clyde import Clyde
from hero import CapMan

pygame.init()
screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
running = True

player = pygame.sprite.GroupSingle()
player.add(CapMan())

pinky = pygame.sprite.GroupSingle()
pinky.add(Pinky())

clyde = pygame.sprite.GroupSingle()
clyde.add(Clyde())

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        if event.type == pygame.KEYDOWN:
            last_key = player.sprite.checking_Pressed_Keys()
            if last_key != None:
                player.sprite.capman_direction = last_key
                player.sprite.player_rotation(player.sprite.capman_direction)
    screen.fill('black')
    draw_map(screen, grid)
    player.draw(screen)
    player.update(player.sprite.capman_direction)
    pinky.draw(screen)
    clyde.draw(screen)
    pinky.update(player.sprite, (pygame.time.get_ticks() - start_time) / 1000)
    clyde.update(player.sprite, (pygame.time.get_ticks() - start_time) / 1000)
    if pinky.sprite.collision(player.sprite): pygame.quit()
    if clyde.sprite.collision(player.sprite): pygame.quit()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()