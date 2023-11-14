from strategy import MovementStrategy
from common import *
import strategy
from os import path
import pygame

class Enemy:
    x: float
    y: float
    rect: pygame.Rect
    image: pygame.Surface
    movement_strategy: MovementStrategy

    def __init__(self, x,y,image,movement_stategy):
         self.x = x
         self.y = y
         self.rect = image.get_rect()
         self.image = image
         self.movement_strategy = movement_stategy

    def update(self):
        self.movement_strategy.move(self)
        self.rect.bottomleft = (int(self.x),int(self.y))
    

def new_bush(x,y,speed_x):
    _image = pygame.image.load(path.join('assets', 'rosebush.png'))
    image = pygame.transform.scale_by(_image, 2)
    movement_strategy = strategy.BushMovementStrategy(speed_x)
    return Enemy(x, y, image, movement_strategy)

def new_fly(x,y,speed_x):
    _image = pygame.image.load(path.join('assets', 'fly.png'))
    image = pygame.transform.scale_by(_image, 2)
    movement_strategy = strategy.FlyMovementStrategy(speed_x, MAX_Y, PERIOD)
    return Enemy(x, y, image, movement_strategy)

