import pygame
from common import *
import math
from os import path
import random
from enemy import new_bush, new_fly
import strategy
from fox import Fox

def draw_sky_and_ground():
    screen.blit(image_dirt, (0, GROUND))
    screen.blit(image_sky, (0,0))

def draw_text_start():
    text1 = font_big.render('Start' , True, CORAL)
    text2 = font_small.render('Press space to start' , True, BLACK)

    rect1 = text1.get_rect()
    rect1.center = ((WIDTH // 2), (HEIGHT // 2))

    rect2 = text2.get_rect()
    rect2.center = (WIDTH // 2, HEIGHT-40)

    screen.blit(text1, rect1.topleft)
    screen.blit(text2, rect2.topleft)

def draw_text_pause():
    text1 = font_big.render('Pause' , True, CORAL)
    text2 = font_small.render('Press space to continue' , True, BLACK)

    rect1 = text1.get_rect()
    rect1.center = ((WIDTH // 2), (HEIGHT // 2))

    rect2 = text2.get_rect()
    rect2.center = (WIDTH // 2, HEIGHT-40)

    screen.blit(text1, rect1.topleft)
    screen.blit(text2, rect2.topleft)

def draw_text_game_over():
    text1 = font_big.render('GAME OVER' , True, CORAL)
    text2 = font_small.render('Press z to start the game again..' , True, BLACK)

    rect1 = text1.get_rect()
    rect1.center = ((WIDTH // 2), (HEIGHT // 2))

    rect2 = text2.get_rect()
    rect2.center = (WIDTH // 2, HEIGHT-40)

    screen.blit(text1, rect1.topleft)
    screen.blit(text2, rect2.topleft)

def draw_fox(fox):
    screen.blit(fox.image, fox.rect.topleft)

def draw_enemy():
    for enemy in enemies:
            screen.blit(enemy.image, enemy.rect.topleft)
    
def start_event_handler(event):
    global state
    global event_handler
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            state = RUNNING
            event_handler = running_event_handler
       
       
def running_event_handler(event):
    global state
    global event_handler
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            state = PAUSE
            event_handler = pause_event_handler
        elif event.key in [pygame.K_SPACE]:
            fox.process_key(event)
    elif event.type == pygame.KEYUP:
        if event.key in [pygame.K_SPACE]:
            fox.process_key(event)


def pause_event_handler(event):
    global state
    global event_handler
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            state = RUNNING
            event_handler = running_event_handler

    
def game_over_event_handler(event):
    global state
    global event_handler
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            reset_game()
            state = RUNNING
            event_handler = running_event_handler

def reset_game():
    global enemies
    global game_speed
    global scroll_ground
    global scroll_sky
    global enemy_timer
    global fox
    global score

    enemies.clear()
    game_speed = 5.0
    scroll_ground = 0.0
    scroll_sky = 0.0
    enemy_timer = BASE_SPAWN_TIME
    fox.reset()
    score = 0.0

    


# TODO: add pause, menu, game over screen
# TODO: highscore table
# TODO Испраление паузы (и гемовера)
# TODO: animations


pygame.init()


scaled_dims = (WIDTH * SCALE, HEIGHT * SCALE)

display = pygame.display.set_mode(scaled_dims)
screen = pygame.Surface((WIDTH, HEIGHT))

game_speed = 5.0
enemy_timer = BASE_SPAWN_TIME

fox = Fox(GROUND)
enemies = []
score = 0

event_handler = start_event_handler


font = pygame.font.Font(path.join("assets", "prstart.ttf"), 24)
font_big = pygame.font.Font(path.join("assets", "prstart.ttf"), 50)
font_small = pygame.font.Font(path.join("assets", "prstart.ttf"), 15)

image_sky = pygame.image.load(path.join("assets", "sky.png"))
image_dirt = pygame.image.load(path.join("assets", "dirt.png"))

image_width = image_dirt.get_width()
tiles = math.ceil(WIDTH / image_width) + 1

clock = pygame.time.Clock()

state = START

def spawn_enemy():
    choice = random.randint(1, 4)
    print(choice)
    offset = random.randint(-BOUND, BOUND)
    if choice == 1 or choice == 2:
        enemies.append(new_bush(WIDTH + BOUND + offset, GROUND, game_speed))
    elif choice == 3:
        sphread = random.randint(10, 30             )
        enemies.append(new_bush(WIDTH + BOUND, GROUND, game_speed))
        enemies.append(new_bush(WIDTH + BOUND + sphread, GROUND, game_speed))
        enemies.append(new_bush(WIDTH + BOUND + 2 * sphread, GROUND, game_speed))
    elif choice == 4:
        fly_y = 100
        enemies.append(new_fly(WIDTH, GROUND - fly_y, game_speed))
        # spawn fly

scroll_ground = 0.0
scroll_sky = 0.0

is_running = True
while is_running:

    current_event_handler = event_handler

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        else:
            current_event_handler(event)
            

    if state == START:
        draw_sky_and_ground()
        draw_text_start()
        draw_fox(fox)
          
    elif state == RUNNING:
         # updating
        game_speed += GAME_SPEED_GROW_FACTOR

        
        enemy_timer += 1
        if enemy_timer >= BASE_SPAWN_TIME / game_speed:
            spawn_enemy()
            enemy_timer = 0

        fox.update()
        score += game_speed / (FPS * 4)
        
        for enemy in enemies:
            enemy.update()
            if enemy.rect.right < 0:
                enemies.remove(enemy)

            if enemy.rect.colliderect(fox.rect):
                state = GAME_OVER
                #is_running = False
        
        # drawing
        #screen.fill((70, 140, 200))
        for tile in range (tiles):
            screen.blit(image_dirt, (tile*WIDTH - int(scroll_ground), GROUND))
            screen.blit(image_sky, (tile*WIDTH - int(scroll_sky),0))
        
        scroll_ground += game_speed
        scroll_sky += 0.5
        if(scroll_ground >= image_width):
            scroll_ground = 0
        
        if(scroll_sky >= image_width):
            scroll_sky = 0      

        screen.blit(fox.image, fox.rect.topleft)

        draw_enemy()
        
        text = font.render('SCORE:' + ' '+ str(  round(score)), True, CORAL)
        screen.blit(text, (0, 2))
    elif state == PAUSE:
        draw_fox(fox)
        draw_enemy()
        draw_text_pause()
    elif state == GAME_OVER:
        draw_fox(fox)
        draw_enemy()
        draw_text_game_over()



    display.blit(pygame.transform.scale(screen, (WIDTH * SCALE, HEIGHT * SCALE)), (0, 0))
    pygame.display.update()
    
    clock.tick(FPS)

pygame.quit()

