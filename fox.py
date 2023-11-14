import pygame
from os import path
from common import *

class Fox:
    image: pygame.Surface
    rect: pygame.Rect
    y: float
    speed_y: int
    accel_y: int
    is_jumping: bool
    ground: int

    def __init__(self, ground: int) -> None:
        self.ground = ground

        image: pygame.Surface = pygame.image.load(
            path.join("assets", "fox.png")
        ).convert_alpha()
        self.image = pygame.transform.scale_by(image, 2)

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (100, ground)

        self.y = ground 
        self.speed_y = 0
        self.accel_y = 1

        self.is_jumping = False

    def update(self) -> None:
        if self.is_jumping:
            self.jump()

        self.speed_y += self.accel_y
        self.y += self.speed_y

        if self.y >= self.ground:
            self.y = self.ground
            self.speed_y = 0

        self.rect.bottomleft = (100, int(self.y))

    def jump(self) -> None:
        if not self.is_on_ground():
            return    

        self.speed_y = -20

    def is_on_ground(self) -> bool:
        return self.y == self.ground
    
    def reset(self) -> None:
        self.y = self.ground
        self.speed_y = 0

