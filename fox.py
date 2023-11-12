import pygame
from os import path
from common import *

class Fox:
    image: pygame.Surface
    rect: pygame.Rect
    y: int
    speed_y: int
    accel_y: int
    is_jumping: bool

    def __init__(self, GROUND):
        self.GROUND = GROUND

        image = pygame.image.load(path.join("assets", "fox.png"))
        self.image = pygame.transform.scale2x(image)

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (100, GROUND)

        self.y = GROUND
        self.speed_y = 0
        self.accel_y = 1

        self.is_jumping = False

    def update(self):
        if self.is_jumping:
            self.jump()

        self.speed_y += self.accel_y
        self.y += self.speed_y

        if self.y >= self.GROUND:
            self.y = self.GROUND
            self.speed_y = 0

        self.rect.bottomleft = (100, self.y)

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
        return self.y == self.GROUND



