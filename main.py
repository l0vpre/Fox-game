from collections.abc import Callable
from typing import Dict, List, Tuple
import pygame
import math
import common
from os import path
import random
import enemy
from fox import Fox

# TODO: highscore table
# TODO: Испраление паузы (и гемовера)
# TODO: animations

def update_game() -> None:
    global game_speed
    global enemy_timer
    global score

    game_speed += common.GAME_SPEED_GROW_FACTOR
    
    enemy_timer += 1
    if enemy_timer >= common.BASE_SPAWN_TIME / game_speed:
        spawn_enemy()
        enemy_timer = 0
    
    score += game_speed / (common.FPS * 4)

def update_physics() -> None:
    global state
    global event_handler

    fox.update()
    
    for enemy in enemies:
        enemy.update()
        if enemy.rect.right < 0:
            enemies.remove(enemy)
        if enemy.rect.colliderect(fox.rect):
            state = common.GAME_OVER
            event_handler = game_over_event_handler

def update_animations() -> None:
    global scroll_ground
    global scroll_sky

    scroll_ground += game_speed
    scroll_sky += 0.5
    if(scroll_ground >= image_width):
        scroll_ground = 0
    
    if(scroll_sky >= image_width):
        scroll_sky = 0      

def spawn_enemy() -> None:
    choice: int = random.randint(1, 4)
    offset: int = random.randint(-common.BOUND, common.BOUND)
    if choice == 1 or choice == 2:
        enemies.append(enemy.new_bush(common.WIDTH + common.BOUND + offset, common.GROUND, game_speed))
    elif choice == 3:
        sphread: int = random.randint(10, 30             )
        enemies.append(enemy.new_bush(common.WIDTH + common.BOUND, common.GROUND, game_speed))
        enemies.append(enemy.new_bush(common.WIDTH + common.BOUND + sphread, common.GROUND, game_speed))
        enemies.append(enemy.new_bush(common.WIDTH + common.BOUND + 2 * sphread, common.GROUND, game_speed))
    elif choice == 4:
        fly_y: int = 100
        enemies.append(enemy.new_fly(common.WIDTH, common.GROUND - fly_y, game_speed))

def draw_background() -> None:
    for tile in range (tiles):
        screen.blit(image_dirt, (tile * common.WIDTH - int(scroll_ground), common.GROUND))
        screen.blit(image_sky, (tile * common.WIDTH - int(scroll_sky), 0))

def draw_text_start() -> None:
    text1: pygame.surface.Surface = font_big.render('Start' , True, common.CORAL)
    text2: pygame.surface.Surface = font_small.render('Press space to start' , True, common.BLACK)

    rect1: pygame.Rect = text1.get_rect()
    rect1.center = (int(common.WIDTH // 2), int(common.HEIGHT // 2))

    rect2: pygame.Rect = text2.get_rect()
    rect2.center = (int(common.WIDTH // 2), int(common.HEIGHT-40))

    screen.blit(text1, rect1.topleft)
    screen.blit(text2, rect2.topleft)

def draw_text_pause() -> None:
    text1: pygame.surface.Surface = font_big.render('Pause' , True, common.CORAL)
    text2: pygame.surface.Surface = font_small.render('Press space to continue' , True, common.BLACK)

    rect1:pygame.Rect = text1.get_rect()
    rect1.center = (common.WIDTH // 2, common.HEIGHT // 2)

    rect2: pygame.Rect = text2.get_rect()
    rect2.center = (common.WIDTH // 2, common.HEIGHT - 40)

    screen.blit(text1, rect1.topleft)
    screen.blit(text2, rect2.topleft)

def draw_text_game_over() -> None:
    text1: pygame.surface.Surface = font_big.render('GAME OVER' , True, common.CORAL)
    text2: pygame.surface.Surface = font_small.render('Press SPACE to start the game again..' , True, common.BLACK)

    rect1: pygame.Rect = text1.get_rect()
    rect1.center = (common.WIDTH // 2, common.HEIGHT // 2)

    rect2: pygame.Rect = text2.get_rect()
    rect2.center = (common.WIDTH // 2, common.HEIGHT - 40)

    screen.blit(text1, rect1.topleft)
    screen.blit(text2, rect2.topleft)

def draw_score():
    text: pygame.surface.Surface = font.render('SCORE:' + ' '+ str(  round(score)), True, common.CORAL)
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
            state = common.RUNNING
       
def running_event_handler(event):
    global state
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            state = common.PAUSE
        elif event.key == pygame.K_SPACE:
            fox.is_jumping = True
    elif event.type == pygame.KEYUP:
        if event.key== pygame.K_SPACE:
            fox.is_jumping = False

def pause_event_handler(event):
    global state
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            state = common.RUNNING
    
def game_over_event_handler(event):
    global state
    global event_handler
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            reset_game()
            state = common.RUNNING

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
    enemy_timer = common.BASE_SPAWN_TIME
    fox.reset()
    score = 0.0

pygame.init()
enemy.load_images()

# display
scaled_dims: (Tuple[int, int]) = (common.WIDTH * common.SCALE, common.HEIGHT * common.SCALE)
display: pygame.surface.Surface = pygame.display.set_mode(scaled_dims)
screen: pygame.surface.Surface = pygame.Surface((common.WIDTH, common.HEIGHT))

# game
game_speed: float = 5.0
enemy_timer: float = common.BASE_SPAWN_TIME
score: float = 0
highscore: float = 0 # TODO: show score and highscore on game over screen
state: int = common.START
clock: pygame.time.Clock = pygame.time.Clock()

# event handlers
event_handlers: Dict[int, Callable[[pygame.event.Event], None]] = {
    common.START: start_event_handler,
    common.RUNNING: running_event_handler,
    common.PAUSE: pause_event_handler,
    common.GAME_OVER: game_over_event_handler
}

# entities
fox: Fox = Fox(common.GROUND)
enemies: List[enemy.Enemy] = []

# graphics
font: pygame.font.Font = pygame.font.Font(path.join("assets", "prstart.ttf"), 24)
font_big: pygame.font.Font = pygame.font.Font(path.join("assets", "prstart.ttf"), 50)
font_small: pygame.font.Font = pygame.font.Font(path.join("assets", "prstart.ttf"), 15)

image_sky: pygame.surface.Surface = pygame.image.load(
    path.join("assets", "sky.png")
).convert_alpha()
image_dirt: pygame.surface.Surface = pygame.image.load(
    path.join("assets", "dirt.png")
).convert_alpha()

image_width: int = image_dirt.get_width()
tiles: int = math.ceil(common.WIDTH / image_width) + 1

scroll_ground: float = 0.0
scroll_sky: float = 0.0

is_running: bool = True
while is_running:
    event_handler: Callable[[pygame.event.Event], None] = event_handlers[state]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        else:
            event_handler(event)
            
    draw_background()

    if state == common.START:
        draw_text_start()
        draw_fox()
          
    elif state == common.RUNNING:
        update_game()
        update_physics()
        update_animations()
        draw_score()
        draw_fox()
        draw_enemy()
        
    elif state == common.PAUSE:
        draw_fox()
        draw_enemy()
        draw_text_pause()
        draw_score()

    elif state == common.GAME_OVER:
        draw_fox()
        draw_enemy()
        draw_text_game_over()

    display.blit(pygame.transform.scale(screen, (common.WIDTH * common.SCALE, common.HEIGHT * common.SCALE)), (0, 0))
    pygame.display.update()
    
    clock.tick(common.FPS)
    

pygame.quit()

