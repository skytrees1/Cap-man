import pygame
from sys import exit
#Stworzenie klasy CapMan
class CapMan(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #Ilość serduszek
        self.hearts = 2
        #Prędkość z jaką Cap-Man będzie się poruszał (pixels per frame)
        self.speed = 2
        #Pomocniczy obrazek, do zmiany
        self.image = pygame.image.load('../zdj/cap_man_1.png').convert_alpha()
        #Podstawowa pozycja Cap - Mana
        self.rect = self.image.get_rect(center = (200,500))
    def player_movement(self, pressed_key):
        #Porusza się w odpowiednim kierunku pod warunkiem że środek jest na ekranie
        #Oraz nie zostanie wciśnięty inny klawisz
        if (pressed_key == pygame.K_UP or pressed_key == pygame.K_w) and self.rect.centery > 0:
            self.rect.y -= self.speed
        elif (pressed_key == pygame.K_DOWN or pressed_key == pygame.K_s) and self.rect.centery < 680:
            self.rect.y += self.speed
        elif (pressed_key == pygame.K_RIGHT or pressed_key == pygame.K_d) and self.rect.centerx > 0:
            self.rect.x += self.speed
        elif (pressed_key == pygame.K_LEFT or pressed_key == pygame.K_a) and self.rect.centerx < 920:
            self.rect.x -= self.speed
    @staticmethod
    def checking_Pressed_Keys():
        #Zwraca obecnie wciśnięty klawisz, jeżeli jest jednym z tych które bierzemy pod uwagę
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            return pygame.K_UP
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            return pygame.K_DOWN
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            return pygame.K_RIGHT
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            return pygame.K_LEFT
        return None
    def update(self,pressed_key):
        self.player_movement(pressed_key)
    #Funkcje do zwiększenia i zmniejszenia prędkości 
    def increase_speed(self):
        self.speed += 2
    def reduce_speed(self):
        self.speed -= 2

        
pygame.init()

screen = pygame.display.set_mode((920,680))
clock = pygame.time.Clock()
running = True
#Potrzebna zmienna nr.1
PRESSED_KEY = None
#Stworzenie naszej postaci, przed główną pętlą gry
player = pygame.sprite.GroupSingle()
player.add(CapMan())
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        #Potrzebne do poprawnego funkcjonowania
        if event.type == pygame.KEYDOWN:
            last_key = player.sprite.checking_Pressed_Keys()
            if last_key != None:
                PRESSED_KEY = last_key
    screen.fill("Purple")
    #Narysowanie Cap-Mana na ekranie
    player.draw(screen)
    #Aktualizuje co robimy z naszą postacią
    player.update(PRESSED_KEY)
    #
    pygame.display.flip()
    #Testowe odwołanie się do zmiennej hearts oraz zmiana jej wartości
    #Po podanym warunku Postać się zatrzymuje (pressed_key = None) i potem można dalej ustawić kierunek
    # player.sprite.hearts -= 1
    # if player.sprite.hearts  == -150:
    #Poprawnie działa increase_speed()
        # player.sprite.increase_speed()
    #     pressed_key = None
    # print(player.sprite.hearts)
    clock.tick(60)
pygame.quit()