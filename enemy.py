from abc import abstractmethod
from common import *
from os import path
import pygame
import math

class MovementStrategy:
    @abstractmethod
    def move(self, enemy: "Enemy") -> None: ...


class BushMovementStrategy(MovementStrategy):
    speed: float

    def __init__(self, speed: float) -> None:
        self.speed = speed

    def move(self, enemy: "Enemy") -> None:
        enemy.x -= self.speed
    

class FlyMovementStrategy(MovementStrategy):
    speed_x: float
    max_y: float
    frequency: float
    frame: float

    def __init__(self, speed_x: float, max_y: float, period: float) -> None:
        self.speed_x = speed_x
        self.frequency = 2 * math.pi / period
        self.max_y = max_y/FPS
        self.frame = 0.0

    def move(self, enemy: "Enemy") -> None:
        enemy.x -= self.speed_x
        time: float = self.frame / FPS
        enemy.y += self.max_y * self.frequency * math.cos(time * self.frequency)
        self.frame += 1


class Enemy:
    x: float
    y: float
    rect: pygame.Rect
    image: pygame.Surface
    movement_strategy: MovementStrategy

    def __init__(self,
             x: float,
             y: float,
             image: pygame.Surface,
             movement_stategy: MovementStrategy) -> None:
         self.x = x
         self.y = y
         self.rect = image.get_rect()
         self.image = image
         self.movement_strategy = movement_stategy

    def update(self) -> None:
        self.movement_strategy.move(self)
        self.rect.bottomleft = (int(self.x),int(self.y))
    

def new_bush(x: float, y: float, speed_x: float) -> Enemy:
    image: pygame.Surface = pygame.image.load(path.join('assets', 'rosebush.png'))
    image = pygame.transform.scale_by(image, 2)

    movement_strategy: MovementStrategy = BushMovementStrategy(speed_x)

    return Enemy(x, y, image, movement_strategy)

def new_fly(x: float, y: float, speed_x: float) -> Enemy:
    image: pygame.Surface = pygame.image.load(path.join('assets', 'fly.png'))
    image = pygame.transform.scale_by(image, 2)

    movement_strategy: MovementStrategy = FlyMovementStrategy(speed_x, MAX_Y, PERIOD)

    return Enemy(x, y, image, movement_strategy)

