from typing import Tuple


WIDTH: int = 800
HEIGHT: int = 600
SCALE: int = 1
GROUND: int = 450
GAME_SPEED_GROW_FACTOR: float = 0.001
BASE_SPAWN_TIME: float = 1500
BOUND: int = 100
FPS: float = 60
MAX_Y: int = 25
PERIOD: float = 1

CORAL: Tuple[int, int, int] = (240, 117, 87)
BLACK: Tuple[int, int, int] = (0,0,0)

START: int = 1
RUNNING: int = 2
PAUSE: int = 3
GAME_OVER: int = 4
