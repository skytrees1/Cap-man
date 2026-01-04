import pygame
#Stworzenie klasy CapMan
class CapMan(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('../zdj/cap_man_1.png').convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (200,500))
pygame.init()

screen = pygame.display.set_mode((920,680))
clock = pygame.time.Clock()
running = True
#Stworzenie naszej postaci, przed główną pętlą gry
player = pygame.sprite.GroupSingle()
player.add(CapMan())
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("Purple")
    #Narysowanie Cap-Mana na ekranie
    player.draw(screen)
    pygame.display.flip()

    clock.tick(60)
pygame.quit()