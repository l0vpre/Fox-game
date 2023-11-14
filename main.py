import pygame
from common import *
import math
from os import path
import random
from enemy import new_bush, new_fly
from fox import Fox

# TODO: highscore table
# TODO: Испраление паузы (и гемовера)
# TODO: animations

def update_game():
    global game_speed
    global enemy_timer
    global score

    game_speed += GAME_SPEED_GROW_FACTOR
    
    enemy_timer += 1
    if enemy_timer >= BASE_SPAWN_TIME / game_speed:
        spawn_enemy()
        enemy_timer = 0
    
    score += game_speed / (FPS * 4)

def update_physics():
    global state
    global event_handler

    fox.update()
    
    for enemy in enemies:
        enemy.update()
        if enemy.rect.right < 0:
            enemies.remove(enemy)
        if enemy.rect.colliderect(fox.rect):
            state = GAME_OVER
            event_handler = game_over_event_handler

def update_animations():
    global scroll_ground
    global scroll_sky

    scroll_ground += game_speed
    scroll_sky += 0.5
    if(scroll_ground >= image_width):
        scroll_ground = 0
    
    if(scroll_sky >= image_width):
        scroll_sky = 0      

def spawn_enemy():
    choice = random.randint(1, 4)
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

def draw_background():
    for tile in range (tiles):
        screen.blit(image_dirt, (tile*WIDTH - int(scroll_ground), GROUND))
        screen.blit(image_sky, (tile*WIDTH - int(scroll_sky),0))

def draw_text_start():
    text1 = font_big.render('Start' , True, CORAL)
    text2 = font_small.render('Press space to start' , True, BLACK)

    rect1 = text1.get_rect()
    rect1.center = (int(WIDTH // 2), int(HEIGHT // 2))

    rect2 = text2.get_rect()
    rect2.center = (int(WIDTH // 2), int(HEIGHT-40))

    screen.blit(text1, rect1.topleft)
    screen.blit(text2, rect2.topleft)

def draw_text_pause():
    text1 = font_big.render('Pause' , True, CORAL)
    text2 = font_small.render('Press space to continue' , True, BLACK)

    rect1 = text1.get_rect()
    rect1.center = (WIDTH // 2, HEIGHT // 2)

    rect2 = text2.get_rect()
    rect2.center = (WIDTH // 2, HEIGHT - 40)

    screen.blit(text1, rect1.topleft)
    screen.blit(text2, rect2.topleft)

def draw_text_game_over():
    text1 = font_big.render('GAME OVER' , True, CORAL)
    text2 = font_small.render('Press z to start the game again..' , True, BLACK)

    rect1 = text1.get_rect()
    rect1.center = (WIDTH // 2, HEIGHT // 2)

    rect2 = text2.get_rect()
    rect2.center = (WIDTH // 2, HEIGHT - 40)

    screen.blit(text1, rect1.topleft)
    screen.blit(text2, rect2.topleft)

def draw_score():
    text = font.render('SCORE:' + ' '+ str(  round(score)), True, CORAL)
    screen.blit(text, (0, 2))

def draw_fox():
    screen.blit(fox.image, fox.rect.topleft)

def draw_enemy():
    for enemy in enemies:
            screen.blit(enemy.image, enemy.rect.topleft)
    
def start_event_handler(event):
    global state
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            state = RUNNING
       
def running_event_handler(event):
    global state
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            state = PAUSE
        elif event.key == pygame.K_SPACE:
            fox.is_jumping = True
    elif event.type == pygame.KEYUP:
        if event.key== pygame.K_SPACE:
            fox.is_jumping = False

def pause_event_handler(event):
    global state
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            state = RUNNING
    
def game_over_event_handler(event):
    global state
    global event_handler
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            reset_game()
            state = RUNNING

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

pygame.init()

# display
scaled_dims = (WIDTH * SCALE, HEIGHT * SCALE)
display = pygame.display.set_mode(scaled_dims)
screen = pygame.Surface((WIDTH, HEIGHT))

# game
game_speed = 5.0
enemy_timer = BASE_SPAWN_TIME
score = 0
highscore = 0 # TODO: show score and highscore on game over screen
state = START
clock = pygame.time.Clock()

# event handlers
event_handlers = {
    START: start_event_handler,
    RUNNING: running_event_handler,
    PAUSE: pause_event_handler,
    GAME_OVER: game_over_event_handler
}

# entities
fox = Fox(GROUND)
enemies = []

# graphics
font = pygame.font.Font(path.join("assets", "prstart.ttf"), 24)
font_big = pygame.font.Font(path.join("assets", "prstart.ttf"), 50)
font_small = pygame.font.Font(path.join("assets", "prstart.ttf"), 15)

image_sky = pygame.image.load(path.join("assets", "sky.png"))
image_dirt = pygame.image.load(path.join("assets", "dirt.png"))

image_width = image_dirt.get_width()
tiles = math.ceil(WIDTH / image_width) + 1

scroll_ground = 0.0
scroll_sky = 0.0

is_running = True
while is_running:
    event_handler = event_handlers[state]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        else:
            event_handler(event)
            
    draw_background()

    if state == START:
        draw_text_start()
        draw_fox()
          
    elif state == RUNNING:
        update_game()
        update_physics()
        update_animations()
        draw_score()
        draw_fox()
        draw_enemy()
        
    elif state == PAUSE:
        draw_fox()
        draw_enemy()
        draw_text_pause()
        draw_score()

    elif state == GAME_OVER:
        draw_fox()
        draw_enemy()
        draw_text_game_over()

    display.blit(pygame.transform.scale(screen, (WIDTH * SCALE, HEIGHT * SCALE)), (0, 0))
    pygame.display.update()
    
    clock.tick(FPS)

pygame.quit()

