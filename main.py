import pygame
from common import *
from os import path
import random
from enemy import new_bush, new_fly
import strategy
from fox import Fox


# TODO: add pause, menu, game over screen
# TODO: score counter
# TODO: highscore table

# TODO: animations


pygame.init()


scaled_dims = (WIDTH * SCALE, HEIGHT * SCALE)

display = pygame.display.set_mode(scaled_dims)
screen = pygame.Surface((WIDTH, HEIGHT))


enemy_timer = BASE_SPAWN_TIME

fox = Fox(GROUND)
enemies = []


clock = pygame.time.Clock()

def spawn_enemy():
    choice = random.randint(1, 4)
    print(choice)
    offset = random.randint(-BOUND, BOUND)
    if choice == 1 or choice == 2:
        enemies.append(new_bush(WIDTH + BOUND + offset, GROUND, GAME_SPEED))
    elif choice == 3:
        sphread = random.randint(10, 50)
        enemies.append(new_bush(WIDTH + BOUND, GROUND, GAME_SPEED))
        enemies.append(new_bush(WIDTH + BOUND + sphread, GROUND, GAME_SPEED))
        enemies.append(new_bush(WIDTH + BOUND + 2 * sphread, GROUND, GAME_SPEED))
    elif choice == 4:
        fly_y = 100
        enemies.append(new_fly(WIDTH, GROUND - fly_y, GAME_SPEED))
        # spawn fly


image_sky = pygame.image.load(path.join("assets", "sky.png"))
image_dirt = pygame.image.load(path.join("assets", "dirt.png"))
is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key in [pygame.K_SPACE]:
                fox.process_key(event)
           

    # updating
    GAME_SPEED += GAME_SPEED_GROW_FACTOR

    enemy_timer += 1
    if enemy_timer >= BASE_SPAWN_TIME / GAME_SPEED:
        spawn_enemy()
        enemy_timer = 0

    fox.update()
    

    for enemy in enemies:
        enemy.update()
        if enemy.rect.right < 0:
            enemies.remove(enemy)

        if enemy.rect.colliderect(fox.rect):
            pass
            is_running = False

    
    # drawing
    #screen.fill((70, 140, 200))
    screen.blit(image_dirt, (0,GROUND))
    screen.blit(image_sky, (0,0))

    screen.blit(fox.image, fox.rect.topleft)

    

    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect.topleft)

    display.blit(pygame.transform.scale(screen, (WIDTH * SCALE, HEIGHT * SCALE)), (0, 0))
    pygame.display.update()
    clock.tick(FPS)




pygame.quit()
