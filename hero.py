import pygame as p
from CONST import *
from map_generator import level

#Stworzenie klasy CapMan

class CapMan(p.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.direction = None
        self.capman_direction = None
        self.hearts = 2 #Ilość serduszek
        self.speed = 3 #Prędkość
        self.rage = False  # Tryb zjadania duszków
        #Pomocniczy obrazek, do zmiany

        self.angle = 0
        self.image = p.image.load('assets/images/cap_man_1_1.png').convert_alpha()
        self.image = p.transform.scale(self.image,(45,45)) 

        #Podstawowa pozycja Cap - Mana na obecnej mapie

        self.rect = self.image.get_rect(center = (STARTING_POSITION_X,STARTING_POSITION_Y))


    def player_movement(self, direction, turns):
        #Porusza się w odpowiednim kierunku pod warunkiem że środek jest na ekranie
        #Oraz nie zostanie wciśnięty inny klawisz

        center_x = (self.rect.centerx // TILE_SIZE_X) * TILE_SIZE_X + (TILE_SIZE_X // 2)
        center_y = (self.rect.centery // TILE_SIZE_Y) * TILE_SIZE_Y + (TILE_SIZE_Y // 2)

        if direction == "move_up" and turns[2]:
            self.rect.y -= self.speed
            self.rect.centerx = center_x
        elif direction == "move_down" and turns[3]:
            self.rect.y += self.speed
            self.rect.centerx = center_x
        elif direction == "move_right" and turns[0]:
            self.rect.x += self.speed
            self.rect.centery = center_y
        elif direction == "move_left" and turns[1]:
            self.rect.x -= self.speed
            self.rect.centery = center_y


    def player_rotation(self, direction):
        #Oraz nie zostanie wciśnięty inny klawisz
        # 0 stopni - porusza się w prawo
        # 90 stopni - porusza się w dół
        # 270 stopni - porusza się w górę
        # 180 stopni - porusza się w lewo
        # rotated = p.transform.rotate(self.image, self.angle)

        turns = self.check_position(direction)
        if direction == "move_up" and turns[2]:
            if self.angle == 90:
                self.image = p.transform.flip(self.image,False, True)
            elif self.angle == 0:
                self.image = p.transform.rotate(self.image, 90)
            elif self.angle == 180:
                self.image = p.transform.rotate(self.image, -90)
                self.image = p.transform.flip(self.image,True, False)
            self.angle = 270
        elif direction == "move_down" and turns[3]:
            if self.angle == 0:
                self.image = p.transform.rotate(self.image, -90)
                self.image = p.transform.flip(self.image,True, False)
            elif self.angle == 270:
                self.image = p.transform.flip(self.image,False, True)
            elif self.angle == 180:
                self.image = p.transform.rotate(self.image, 90)
            self.angle = 90
        elif direction == "move_right" and turns[0]:
            if self.angle == 180:
                self.image = p.transform.flip(self.image,True, False)
            elif self.angle == 270:
                self.image = p.transform.rotate(self.image, -90)
            elif self.angle == 90:
                self.image = p.transform.flip(self.image,False, True)
                self.image = p.transform.rotate(self.image, -90)
            self.angle = 0
        elif direction == "move_left" and turns[1]:
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
        #Zwraca obecnie kierunek, jeżeli jest jednym z tych które bierzemy pod uwagę
        keys = p.key.get_pressed()
        if keys[p.K_UP] or keys[p.K_w]:
            return "move_up"
        elif keys[p.K_DOWN] or keys[p.K_s]:
            return "move_down"
        elif keys[p.K_RIGHT] or keys[p.K_d]:
            return "move_right"
        elif keys[p.K_LEFT] or keys[p.K_a]:
            return "move_left"
        return None
    #Zmienia kierunek poruszania się postaci


    def update(self, direction):
        turns = self.check_position(direction)
        self.player_movement(direction, turns)

        # TELEPORT TUNELU 

        if self.rect.centerx > WIDTH - 10:
            self.rect.centerx = 10
        elif self.rect.centerx < 10:
            self.rect.centerx = WIDTH - 10
        
    #Funkcje do zwiększenia i zmniejszenia prędkości 

    def increase_speed(self):
        self.speed += 1


    def reduce_speed(self):
        self.speed -= 1


    def check_position(self,direction):
        turns = [False, False, False, False] # turns = [right, left, up, down]

        num1 = TILE_SIZE_Y      # wysokość kafelka
        num2 = TILE_SIZE_X      # szerokość kafelka
        num3 = num2 // 2        # połowa kafelka 

        max_y = len(level)      # ilość kafelek w pionie
        max_x = len(level[0])   # ilość kafelek w poziomie

        def safe(y, x):
            # y w zakresie, x może się zawijać (tunel)
            if 0 <= y < max_y:
                x = x % max_x
                return level[y][x] in ('a', 'o', 'n')
            return False

        # indeksy kafelka, na którym jest środek CapMana
        tile_x = self.rect.centerx // num2
        tile_y = self.rect.centery // num1

        # jeśli jesteśmy "w normalnej planszy", nie w tunelu
        if tile_x < max_x - 1:

            # --- PODSTAWOWE SPRAWDZENIA W 4 KIERUNKACH ---

            if direction == "move_right":
                # patrzymy w PRAWO (+num3) i ustawiamy turns[0] (prawo)
                if safe(tile_y, (self.rect.centerx + num3) // num2):
                    turns[0] = True

            if direction == "move_left":
                # patrzymy w LEWO (-num3) i ustawiamy turns[1] (lewo)
                if safe(tile_y, (self.rect.centerx - num3) // num2):
                    turns[1] = True

            if direction == "move_up":
                # patrzymy w GÓRĘ (-num3) i ustawiamy turns[2] (góra)
                if safe((self.rect.centery - num3) // num1, self.rect.centerx // num2):
                    turns[2] = True

            if direction == "move_down":
                # patrzymy w DÓŁ (+num3) i ustawiamy turns[3] (dół)
                if safe((self.rect.centery + num3) // num1, self.rect.centerx // num2):
                    turns[3] = True

            offset_x = self.rect.centerx % num2
            offset_y = self.rect.centery % num1
            #Margines błędu środka CapMana kiedy możemy zmienić kierunek
            center_min = num2 // 2 - 3   
            center_max = num2 // 2 + 3   

            # jeśli poruszamy się pionowo i jesteśmy prawie na środku w poziomie
            if direction in ("move_up", "move_down"):
                if center_min <= offset_x <= center_max:
                    # kontynuacja góra/dół
                    if safe((self.rect.centery - num3) // num1, self.rect.centerx // num2):
                        turns[2] = True
                    if safe((self.rect.centery + num3) // num1, self.rect.centerx // num2):
                        turns[3] = True

                # jeśli jesteśmy prawie na środku w pionie – można skręcić lewo/prawo
                if center_min <= offset_y <= center_max:
                    if safe(self.rect.centery // num1, (self.rect.centerx - num2) // num2):
                        turns[1] = True  # lewo
                    if safe(self.rect.centery // num1, (self.rect.centerx + num2) // num2):
                        turns[0] = True  # prawo

            # jeśli poruszamy się poziomo i jesteśmy prawie na środku w poziomie
            if direction in ("move_right", "move_left"):
                if center_min <= offset_x <= center_max:
                    if safe((self.rect.centery - num1) // num1, self.rect.centerx // num2):
                        turns[2] = True  # góra
                    if safe((self.rect.centery + num1) // num1, self.rect.centerx // num2):
                        turns[3] = True  # dół

                if center_min <= offset_y <= center_max:
                    if safe(self.rect.centery // num1, (self.rect.centerx - num3) // num2):
                        turns[1] = True  # lewo
                    if safe(self.rect.centery // num1, (self.rect.centerx + num3) // num2):
                        turns[0] = True  # prawo

        else:
            # tunel – w poziomie zawsze można
            turns[0] = True
            turns[1] = True

        return turns
    