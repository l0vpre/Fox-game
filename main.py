from os import path
import random

import pygame

# TODO: add fly
# TODO: fix sprites
# TODO: add pause, menu, game over screen
# TODO: score counter
# TODO: highscore table
# TODO: draw ground and sky
# TODO: animations

class Fox:
    image: pygame.Surface
    rect: pygame.Rect
    y: int
    speed_y: int
    accel_y: int
    is_jumping: bool

    def __init__(self, ground):
        self.ground = ground

        image = pygame.image.load(path.join("assets", "fox.png"))
        self.image = pygame.transform.scale2x(image)

        self.rect = self.image.get_rect()
        self.rect.center = (100, ground)

        self.y = ground
        self.speed_y = 0
        self.accel_y = 1

        self.is_jumping = False

    def update(self):
        if self.is_jumping:
            self.jump()

        self.speed_y += self.accel_y
        self.y += self.speed_y

        if self.y >= self.ground:
            self.y = self.ground
            self.speed_y = 0

        self.rect.center = (100, self.y)

    def process_key(self, event):
        if event.key == pygame.K_SPACE:
            if event.type == pygame.KEYDOWN:
                self.is_jumping = True
            elif event.type == pygame.KEYUP:
                self.is_jumping = False

    def jump(self):
        if not self.is_on_ground():
            return    

        self.speed_y = -20

    def is_on_ground(self):
        return self.y == self.ground


class Cactus:
    image: pygame.Surface
    rect: pygame.Rect
    x: int
    speed_x: int

    def __init__(self, x, y, speed_x):
        image = pygame.image.load(path.join('assets', 'cactus.png'))
        self.image = pygame.transform.scale_by(image, 2)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed_x = speed_x

    def update(self):
        x, y = self.rect.topleft
        x -= self.speed_x
        self.rect.topleft = (x, y)



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
        enemies.append(Cactus(width + bound + offset, ground, game_speed))
    elif choice == 3:
        sphread = random.randint(10, 50)
        enemies.append(Cactus(width + bound, ground, game_speed))
        enemies.append(Cactus(width + bound + sphread, ground, game_speed))
        enemies.append(Cactus(width + bound + 2 * sphread, ground, game_speed))
    elif choice == 4:
        fly_y = 100
        enemies.append(Cactus(width, ground - fly_y, game_speed))
        # spawn fly



is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key in [pygame.K_SPACE]:
                fox.process_key(event)
           

    # updating
    game_speed += 0.0005

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
            # is_running = False

    
    # drawing
    screen.fill((70, 140, 200))

    screen.blit(fox.image, fox.rect.topleft)

    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect.topleft)

    display.blit(pygame.transform.scale(screen, (width * scale, height * scale)), (0, 0))
    pygame.display.update()
    clock.tick(60)
    

pygame.quit()
