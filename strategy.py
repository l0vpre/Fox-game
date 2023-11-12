import math
from common import *

class MovementStrategy:
   def move(self, enemy):
       pass


class BushMovementStrategy(MovementStrategy):
   speed: float

   def __init__(self, speed):
         self.speed = speed


   def move(self, enemy):
         enemy.x -= self.speed
    

class FlyMovementStrategy(MovementStrategy):
   speed_x: float
   max_y: float
   frequency: float
   FPS: float
   frame: float

   def __init__(self, speed_x,max_y, period):
         self.speed_x = speed_x
         self.frequency = 2*math.pi / period
         self.FPS = FPS
         self.max_y = max_y/self.FPS
         self.frame = 0.0

   def move(self, enemy):
         enemy.x -= self.speed_x
         time = self.frame / self.FPS
         speed_y = self.max_y* self.frequency * math.cos(time*self.frequency)
         enemy.y += speed_y
         self.frame += 1