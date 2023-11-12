import pygame
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

width, height = 800, 600
scale = 1
scaled_dims = (width * scale, height * scale)

display = pygame.display.set_mode(scaled_dims)
screen = pygame.Surface((width, height))

ground = 450
game_speed = 5.0
base_spawn_time = 1500
enemy_timer = base_spawn_time

fox = Fox(ground)
enemies = []


clock = pygame.time.Clock()

def spawn_enemy():
    choice = random.randint(1, 4)
    bound = 100
    print(choice)
    offset = random.randint(-bound, bound)
    if choice == 1 or choice == 2:
        enemies.append(new_bush(width + bound + offset, ground, game_speed))
    elif choice == 3:
        sphread = random.randint(10, 50)
        enemies.append(new_bush(width + bound, ground, game_speed))
        enemies.append(new_bush(width + bound + sphread, ground, game_speed))
        enemies.append(new_bush(width + bound + 2 * sphread, ground, game_speed))
    elif choice == 4:
        fly_y = 100
        enemies.append(new_fly(width, ground - fly_y, game_speed))
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
    game_speed += 0.001

    enemy_timer += 1
    if enemy_timer >= base_spawn_time / game_speed:
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
    screen.blit(image_dirt, (0,ground))
    screen.blit(image_sky, (0,0))

    screen.blit(fox.image, fox.rect.topleft)

    

    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect.topleft)

    display.blit(pygame.transform.scale(screen, (width * scale, height * scale)), (0, 0))
    pygame.display.update()
    clock.tick(60)




pygame.quit()
