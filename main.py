import pygame
from common import *
import math
from os import path
import random
from enemy import new_bush, new_fly
import strategy
from fox import Fox


# TODO: add pause, menu, game over screen
# TODO: highscore table

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
font = pygame.font.Font(path.join("assets", "prstart.ttf"), 24)

image_sky = pygame.image.load(path.join("assets", "sky.png"))
image_dirt = pygame.image.load(path.join("assets", "dirt.png"))

image_width = image_dirt.get_width()
tiles = math.ceil(WIDTH / image_width) + 1
print(f'sdhksjkd {tiles}')
clock = pygame.time.Clock()

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key in [pygame.K_SPACE]:
                fox.process_key(event)
           

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
            pass
            is_running = False

    
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

    

    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect.topleft)

    text = font.render('SCORE:' + ' '+ str(  round(score)), True, CORAL)
    screen.blit(text, (0, 2))

    display.blit(pygame.transform.scale(screen, (WIDTH * SCALE, HEIGHT * SCALE)), (0, 0))
    pygame.display.update()
    
    clock.tick(FPS)


         

pygame.quit()
