"""
Pętla główna gry
"""


import pygame as p
import copy
from board import board
from CONST import *
from map_generator import draw_map
from hero import CapMan
from pinky import Pinky
from clyde import Clyde
from red import red
from inky import inky

p.init()
p.mixer.init()

screen = p.display.set_mode((WIDTH, HEIGHT), p.RESIZABLE)
game_screen = p.Surface((WIDTH, HEIGHT))
clock = p.time.Clock()

MUSIC_MAIN = None
MUSIC_FRIGHTENED = None
sfx_dot = None
sfx_power = None
sfx_eat_ghost = None
sfx_death = None

# Klasa atrapa (używana gdy nie ma pliku dźwiękowego)
class DummySound:
    def play(self): pass
    def set_volume(self, v): pass

# --- 2. ŁADOWANIE PLIKÓW DŹWIĘKOWYCH ---
print("--- Próba ładowania dźwięków ---")
try:
   
    MUSIC_MAIN = 'assets/sounds/charge.ogg'           
    MUSIC_FRIGHTENED = 'assets/sounds/mystical.mp3' 

    
    try: sfx_dot = p.mixer.Sound('assets/sounds/Picked Coin Echo 2.wav'); sfx_dot.set_volume(0.2)
    except: sfx_dot = DummySound(); print("Brak pliku: sfx_dot.wav")

    try: sfx_power = p.mixer.Sound('assets/sounds/Power Up.wav'); sfx_power.set_volume(0.4)
    except: sfx_power = DummySound(); print("Brak pliku: sfx_power.wav")

    try: sfx_eat_ghost = p.mixer.Sound('assets/sounds/Win sound.wav'); sfx_eat_ghost.set_volume(1.5)
    except: sfx_eat_ghost = DummySound(); print("Brak pliku: sfx_eat_ghost.wav")

    try: sfx_death = p.mixer.Sound('assets/sounds/1.mp3'); sfx_death.set_volume(0.8)
    except: sfx_death = DummySound(); print("Brak pliku: sfx_death.wav")

    print("--- Dźwięki załadowane (te które znaleziono) ---")

except Exception as e:
    print(f"KRYTYCZNY BŁĄD DŹWIĘKU: {e}")
    sfx_dot = sfx_power = sfx_eat_ghost = sfx_death = DummySound()
    MUSIC_MAIN = MUSIC_FRIGHTENED = None


start_time = p.time.get_ticks() #czas dla duszkow

player = p.sprite.GroupSingle()
player.add(CapMan())

pinky = p.sprite.GroupSingle()
pinky.add(Pinky())

clyde = p.sprite.GroupSingle()
clyde.add(Clyde())

ghost_red = p.sprite.GroupSingle()
ghost_red.add(red())

ghost_inky = p.sprite.GroupSingle()
ghost_inky.add(inky())

level = copy.deepcopy(board)

total_dots = sum(row.count('n') + row.count('o') for row in level)

# Zmienne do obsługi punktacji
score = 0
game_font = p.font.Font("assets/fonts/Tiny5-Regular.ttf", 45) 
game_over_font = p.font.Font("assets/fonts/Tiny5-Regular.ttf", 200)
win_font = p.font.Font("assets/fonts/Tiny5-Regular.ttf", 120)
lives = 3

#Zmienne do trybu przestraszenia/FRIGHTENED
is_frightened = False
frightened_start_time = 0
FRIGHTENED_DURATION = 6000 # 6 sekund jak w pacmanie oryginalnym

def reset_positions():
    global start_time
    start_time = p.time.get_ticks()
    is_frightened = False

    if MUSIC_MAIN:
        try:
            p.mixer.music.load(MUSIC_MAIN)
            p.mixer.music.play(-1)
        except Exception as e:
            print(f"Nie udało się odtworzyć muzyki startowej: {e}")

    player.empty()
    pinky.empty()
    clyde.empty()
    ghost_red.empty()
    ghost_inky.empty()

    player.add(CapMan())
    pinky.add(Pinky())
    clyde.add(Clyde())
    ghost_red.add(red())
    ghost_inky.add(inky())

def check_point_collision(player_sprite, current_level, current_score):
    # Obliczamy indeksy kafelka, na którym znajduje się środek gracza
    tile_x = player_sprite.rect.centerx // TILE_SIZE_X
    tile_y = player_sprite.rect.centery // TILE_SIZE_Y

    dots_eaten = 0

    # Zabezpieczenie przed wyjściem poza zakres tablicy
    if 0 <= tile_y < len(current_level) and 0 <= tile_x < len(current_level[0]):
        tile_content = current_level[tile_y][tile_x]

        if tile_content == 'n':      # Mały punkt
            current_level[tile_y][tile_x] = 'a' # Zamień na puste pole ('a')
            sfx_dot.play(maxtime=1000)
            return current_score + 10, False, dots_eaten
        elif tile_content == 'o':    # Duży punkt
            current_level[tile_y][tile_x] = 'a' # Zamień na puste pole ('a')
            sfx_power.play(maxtime=1000)
            return current_score + 50, True, dots_eaten
            
    return current_score, False, 0

def handle_ghost_collision(ghost_sprite, player_sprite):
   
    if ghost_sprite.collision(player_sprite):

        mode = ghost_sprite.mode
        
        # Przypadek 1: Duszek jest już zjedzony (wraca do domu) - ignorujemy kolizję
        if mode == "EATEN":
            return 0
            
        # Przypadek 2: Duszek jest przerażony - ZJADAMY GO
        if mode == "FRIGHTENED":
            # Red i Inky zmieniają się same w swojej metodzie collision, 
            # ale Pinky i Clyde potrzebują pomocy:
            ghost_sprite.mode = "EATEN"
            ghost_sprite.speed = EATEN_SPEED # Stała z CONST.py
            if(ghost_sprite == pinky.sprite or ghost_sprite == clyde.sprite): ghost_sprite.cooldown = BASIC_COOLDOWN
            sfx_eat_ghost.play(maxtime=1000)
            return 200 # Standardowa nagroda za pierwszego duszka
            
        # Przypadek 3: Duszek jest w trybie CHASE lub SCATTER - CapMan ginie
        return -1 # Kod błędu oznaczający śmierć gracza

    return 0 # Brak kolizji

def activate_frightened_mode():
    """Aktywuje tryb przerażenia u wszystkich duszków"""
    global is_frightened, frightened_start_time
    is_frightened = True
    frightened_start_time = p.time.get_ticks()
    
    if MUSIC_FRIGHTENED:
        try:
            p.mixer.music.load(MUSIC_FRIGHTENED)
            p.mixer.music.play(-1)
        except Exception as e:
            print(f"Błąd odtwarzania muzyki FRIGHTENED: {e}")

    # 1. Pinky 
    pinky.sprite.scared()
    
    # 2. Clyde
    clyde.sprite.scared()
    
    # 3. Red (Metoda frighten)
    ghost_red.sprite.frighten()
    
    # 4. Inky (Metoda frighten)
    ghost_inky.sprite.frighten()

def update_ghosts_modes(current_time_sec):
    """Zarządza powrotem do normalnego trybu po upływie czasu"""
    global is_frightened
    
    if is_frightened:
        # Sprawdzamy czy minęło 6 sekund (6000 ms)
        if p.time.get_ticks() - frightened_start_time > FRIGHTENED_DURATION:
            is_frightened = False

            if MUSIC_MAIN:
                try:
                    p.mixer.music.load(MUSIC_MAIN)
                    p.mixer.music.play(-1)
                except: pass

            # Wymuszamy aktualizację trybu na podstawie czasu gry
            # Pinky
            pinky.sprite.unscared(current_time_sec)
            # Clyde
            clyde.sprite.unscared(current_time_sec)
            # Red
            ghost_red.sprite.mode_update(current_time_sec)
            # Inky
            ghost_inky.sprite.mode_update(current_time_sec)

def show_game_final_score():
    overlay = p.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180) # Przezroczystość (0-255)
    overlay.fill((0,0,0))
    game_screen.blit(overlay, (0,0))
    
    text_surf = game_over_font.render("GAME OVER", True, "red")
    score_surf = game_font.render(f"Wynik końcowy: {score}", True, "white")
    
    # Centrowanie napisów
    text_rect = text_surf.get_rect(center=(WIDTH/2, HEIGHT/2 - 100))
    score_rect = score_surf.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
    
    game_screen.blit(text_surf, text_rect)
    game_screen.blit(score_surf, score_rect)

    # Skalowanie obrazu 
    current_w, current_h = screen.get_size()
    scaled_surface = p.transform.smoothscale(game_screen, (current_w, current_h))
    screen.blit(scaled_surface, (0, 0))

    p.display.flip()
    
    # Zamrożenie gry na 3 sekundy
    p.time.delay(3000)

def show_game_win():
    overlay = p.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0,0,0))
    game_screen.blit(overlay, (0,0))
    
    # Napis "GRATULACJE" na złoto/zielono
    text_surf = win_font.render("GRATULACJE", True, "gold")
    subtext_surf = game_font.render("WYGRALES!", True, "white")
    score_surf = game_font.render(f"Wynik końcowy: {score}", True, "white")
    
    text_rect = text_surf.get_rect(center=(WIDTH/2, HEIGHT/2 - 100))
    subtext_rect = subtext_surf.get_rect(center=(WIDTH/2, HEIGHT/2))
    score_rect = score_surf.get_rect(center=(WIDTH/2, HEIGHT/2 + 60))
    
    game_screen.blit(text_surf, text_rect)
    game_screen.blit(subtext_surf, subtext_rect)
    game_screen.blit(score_surf, score_rect)

    current_w, current_h = screen.get_size()
    scaled_surface = p.transform.smoothscale(game_screen, (current_w, current_h))
    screen.blit(scaled_surface, (0, 0))

    p.display.flip()
    p.time.delay(5000)

reset_positions()
running = True

while running:

    current_time_seconds = (p.time.get_ticks() - start_time) / 1000
    
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        elif event.type == p.KEYDOWN:
            if event.key == p.K_ESCAPE:
                running = False
                exit()

            last_key = player.sprite.checking_Pressed_Keys()
            if last_key != None:
                player.sprite.direction = last_key
                player.sprite.player_rotation(player.sprite.direction)

        elif event.type == p.VIDEORESIZE:
            # Aktualizujemy prawdziwy ekran do nowych wymiarów
            width, height = event.w, event.h
            screen = p.display.set_mode((width, height), p.RESIZABLE)

    update_ghosts_modes(current_time_seconds)

    pinky.update(player.sprite, current_time_seconds)
    clyde.update(player.sprite, current_time_seconds)
    ghost_red.update(player.sprite, current_time_seconds)
    ghost_inky.update(player.sprite, ghost_red.sprite, current_time_seconds)

    player.update(player.sprite.direction)

    score, power_pellet, dots_eaten = check_point_collision(player.sprite, level, score)
    total_dots -= dots_eaten

    if power_pellet: activate_frightened_mode()

    if total_dots <= 0:
        p.mixer.music.stop()
       
        sfx_eat_ghost.play() 
        
        game_screen.fill('black')
        draw_map(game_screen, level)
        player.draw(game_screen)
        
        show_game_win()
        running = False
        continue

    death_occured = False

    ghosts_list = [pinky.sprite, clyde.sprite, ghost_red.sprite, ghost_inky.sprite]

    for ghost in ghosts_list:
        result = handle_ghost_collision(ghost, player.sprite)
        
        if result == -1: # Śmierć gracza
            death_occured = True
            break # Przerywamy pętlę, gracz nie żyje
        elif result > 0: # Zjedzono duszka
            score += result
            # Opcjonalnie: dźwięk zjedzenia duszka

    if death_occured:
        lives -= 1
        print(f"HP DOWN\nREAMANING: {lives}")
        p.mixer.music.stop()
        sfx_death.play()
        player.draw(game_screen)
        p.display.flip()

        if lives > 0:
            p.time.delay(1000)
            reset_positions()
        else:
            show_game_final_score()
            running = False

    game_screen.fill('black')
    draw_map(game_screen, level)
    
    player.draw(game_screen)
    pinky.draw(game_screen)
    clyde.draw(game_screen)
    ghost_red.draw(game_screen)
    ghost_inky.draw(game_screen)

    #aktualizacja wyniku
    score_text = game_font.render(f"SCORE: {score}", True, "white")
    game_screen.blit(score_text, (100, HEIGHT - 60))

    lives_text = game_font.render(f"LIVES: {lives}", True, "red")
    game_screen.blit(lives_text, (WIDTH - 300, HEIGHT - 60))

     # skalowanie obrazu 
    current_w, current_h = screen.get_size()
    scaled_surface = p.transform.smoothscale(game_screen, (current_w, current_h))
    screen.blit(scaled_surface, (0, 0))



    p.display.flip()
    clock.tick(60)
p.quit()
